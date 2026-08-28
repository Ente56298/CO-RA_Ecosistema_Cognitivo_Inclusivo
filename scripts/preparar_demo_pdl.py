r"""Prepara capas GeoJSON sanitizadas para el demostrador público PDL.

Uso en Windows PowerShell::

    python scripts/preparar_demo_pdl.py `
      --source-dir "C:\ruta\a\artifacts" `
      --population-csv "C:\ruta\a\localidades_tejupilco_2025-2.csv" `
      --output-dir "data\pdl_demo"

El proceso es determinista, no modifica los originales y sólo conserva
atributos incluidos en las listas blancas declaradas abajo.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import unicodedata
from pathlib import Path
from typing import Any, Iterable


WGS84_BOUNDS = (-180.0, -90.0, 180.0, 90.0)
LAYER_SPECS: dict[str, dict[str, Any]] = {
    "limite_municipal": {
        "source": "limite_municipal_tejupilco.geojson",
        "output": "limite_municipal.geojson",
        "properties": (),
        "evidence_state": "geometria_local_validada_fuente_primaria_pendiente",
    },
    "localidades": {
        "source": "Poligonos_14_Localidades_Tejupilco.geojson",
        "output": "localidades_poblacion.geojson",
        "properties": ("nombre", "area_ha", "vertices"),
        "evidence_state": "geometria_derivada_fuente_primaria_pendiente",
    },
    "colonias": {
        "source": "Colonias_Tejupilco.geojson",
        "output": "colonias.geojson",
        "properties": ("nombre", "cp", "area_ha"),
        "evidence_state": "geometria_derivada_fuente_primaria_pendiente",
    },
    "secciones": {
        "source": "Secciones_46_Oficiales.geojson",
        "output": "secciones_46.geojson",
        "properties": ("seccion", "tipo", "area_ha"),
        "evidence_state": "archivo_local_identificado_como_oficial_localizador_pendiente",
    },
}
LOCALITY_ALIASES = {
    "paso de guayabal": "paso del guayabal",
    "zacatepec": "santo domingo-zacatepec",
}


def sha256_file(path: Path) -> str:
    """Return a file SHA-256 digest without altering the file."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalize_text(value: str) -> str:
    """Normalize a locality label for deterministic joins."""
    base = value.split("(", 1)[0].strip().casefold()
    decomposed = unicodedata.normalize("NFKD", base)
    normalized = "".join(char for char in decomposed if not unicodedata.combining(char))
    collapsed = " ".join(normalized.split())
    return LOCALITY_ALIASES.get(collapsed, collapsed)


def iter_positions(coordinates: Any) -> Iterable[tuple[float, float]]:
    """Yield two-dimensional positions from nested GeoJSON coordinates."""
    if (
        isinstance(coordinates, list)
        and len(coordinates) >= 2
        and isinstance(coordinates[0], (int, float))
        and isinstance(coordinates[1], (int, float))
    ):
        yield float(coordinates[0]), float(coordinates[1])
        return
    if isinstance(coordinates, list):
        for item in coordinates:
            yield from iter_positions(item)


def calculate_bbox(collection: dict[str, Any]) -> list[float]:
    """Calculate and validate a WGS84-compatible bounding box."""
    positions: list[tuple[float, float]] = []
    for feature in collection.get("features", []):
        geometry = feature.get("geometry") or {}
        positions.extend(iter_positions(geometry.get("coordinates", [])))
    if not positions:
        raise ValueError("The layer contains no coordinate positions.")
    xs, ys = zip(*positions)
    bbox = [min(xs), min(ys), max(xs), max(ys)]
    west, south, east, north = WGS84_BOUNDS
    if not (west <= bbox[0] <= east and south <= bbox[1] <= north):
        raise ValueError(f"Coordinates are outside plausible EPSG:4326 bounds: {bbox}")
    if not (west <= bbox[2] <= east and south <= bbox[3] <= north):
        raise ValueError(f"Coordinates are outside plausible EPSG:4326 bounds: {bbox}")
    return [round(value, 6) for value in bbox]


def as_feature_collection(payload: dict[str, Any], layer_name: str) -> dict[str, Any]:
    """Wrap a bare GeoJSON geometry as a one-feature collection."""
    if payload.get("type") == "FeatureCollection":
        return payload
    if payload.get("type") in {"Polygon", "MultiPolygon"}:
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"nombre": layer_name},
                    "geometry": payload,
                }
            ],
        }
    raise ValueError(f"Unsupported GeoJSON root type: {payload.get('type')!r}")


def load_population(csv_path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Load aggregate locality population and its documented source."""
    records: dict[str, dict[str, Any]] = {}
    sources: set[str] = set()
    total_population = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"localidad", "poblacion_total", "pct_del_total_municipal", "fuente"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Population CSV lacks required columns: {sorted(required)}")
        for row in reader:
            name = row["localidad"].strip()
            population = int(float(row["poblacion_total"] or 0))
            share = float(row["pct_del_total_municipal"] or 0)
            source_label = row["fuente"].strip()
            sources.add(source_label)
            total_population += population
            records[normalize_text(name)] = {
                "localidad_fuente": name,
                "poblacion_total": population,
                "pct_total_municipal": share,
                "fuente_poblacion": source_label,
            }
    return records, {
        "rows": len(records),
        "population_sum": total_population,
        "sources": sorted(sources),
        "sha256": sha256_file(csv_path),
    }


def sanitize_layer(
    source_path: Path,
    layer_name: str,
    allowed_properties: tuple[str, ...],
    evidence_state: str,
    population: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    """Return a public GeoJSON layer and unmatched locality labels."""
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    collection = as_feature_collection(payload, layer_name)
    sanitized_features: list[dict[str, Any]] = []
    unmatched: list[str] = []
    for feature in collection.get("features", []):
        geometry = feature.get("geometry")
        if not geometry:
            continue
        source_properties = feature.get("properties") or {}
        properties = {
            key: source_properties.get(key)
            for key in allowed_properties
            if source_properties.get(key) is not None
        }
        if layer_name == "limite_municipal":
            properties["nombre"] = "Tejupilco"
        if layer_name == "localidades":
            locality_name = str(properties.get("nombre", "")).strip()
            population_row = population.get(normalize_text(locality_name))
            if population_row:
                properties.update(population_row)
            else:
                unmatched.append(locality_name)
        properties["capa"] = layer_name
        properties["estado_evidencia"] = evidence_state
        sanitized_features.append(
            {
                "type": "Feature",
                "properties": properties,
                "geometry": geometry,
            }
        )
    sanitized = {
        "type": "FeatureCollection",
        "features": sanitized_features,
    }
    sanitized["bbox"] = calculate_bbox(sanitized)
    sanitized["pdl_meta"] = {
        "layer": layer_name,
        "crs": "EPSG:4326",
        "feature_count": len(sanitized_features),
        "evidence_state": evidence_state,
        "property_whitelist": [
            *allowed_properties,
            *(
                (
                    "localidad_fuente",
                    "poblacion_total",
                    "pct_total_municipal",
                    "fuente_poblacion",
                )
                if layer_name == "localidades"
                else ()
            ),
            "capa",
            "estado_evidencia",
        ],
        "source_sha256": sha256_file(source_path),
    }
    return sanitized, unmatched


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write UTF-8 JSON with stable human-readable formatting."""
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line paths without embedding private locations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--population-csv", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    """Build sanitized layers and an accounting manifest."""
    args = parse_args()
    source_dir: Path = args.source_dir.resolve()
    population_csv: Path = args.population_csv.resolve()
    output_dir: Path = args.output_dir.resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    if not population_csv.is_file():
        raise FileNotFoundError(f"Population CSV does not exist: {population_csv}")
    output_dir.mkdir(parents=True, exist_ok=True)

    population, population_accounting = load_population(population_csv)
    manifest: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_by": "scripts/preparar_demo_pdl.py",
        "crs": "EPSG:4326",
        "population": population_accounting,
        "layers": [],
        "privacy": {
            "personal_records": False,
            "absolute_source_paths": False,
            "property_whitelist_enforced": True,
        },
    }

    for layer_name, spec in LAYER_SPECS.items():
        source_path = source_dir / spec["source"]
        if not source_path.is_file():
            raise FileNotFoundError(f"Required layer does not exist: {spec['source']}")
        sanitized, unmatched = sanitize_layer(
            source_path=source_path,
            layer_name=layer_name,
            allowed_properties=tuple(spec["properties"]),
            evidence_state=str(spec["evidence_state"]),
            population=population,
        )
        output_path = output_dir / spec["output"]
        write_json(output_path, sanitized)
        manifest["layers"].append(
            {
                "id": layer_name,
                "file": spec["output"],
                "features": len(sanitized["features"]),
                "bbox": sanitized["bbox"],
                "evidence_state": spec["evidence_state"],
                "source_sha256": sanitized["pdl_meta"]["source_sha256"],
                "output_sha256": sha256_file(output_path),
                "unmatched_population_labels": unmatched,
            }
        )

    if any(layer["unmatched_population_labels"] for layer in manifest["layers"]):
        raise ValueError("At least one mapped locality could not be joined to population data.")
    if not math.isclose(float(population_accounting["population_sum"]), 79282.0):
        raise ValueError("Population accounting changed from the documented municipal total.")
    write_json(output_dir / "manifest.json", manifest)
    print(
        f"PDL demo prepared: {len(manifest['layers'])} layers, "
        f"{sum(layer['features'] for layer in manifest['layers'])} features."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
