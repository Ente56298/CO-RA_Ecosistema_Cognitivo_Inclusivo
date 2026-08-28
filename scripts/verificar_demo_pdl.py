"""Verifica integridad, privacidad y contabilidad del paquete público PDL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


EXPECTED_COUNTS = {
    "limite_municipal": 1,
    "localidades": 14,
    "colonias": 17,
    "secciones": 46,
}
ALLOWED_PROPERTIES = {
    "limite_municipal": {"nombre", "capa", "estado_evidencia"},
    "localidades": {
        "nombre",
        "area_ha",
        "vertices",
        "localidad_fuente",
        "poblacion_total",
        "pct_total_municipal",
        "fuente_poblacion",
        "capa",
        "estado_evidencia",
    },
    "colonias": {"nombre", "cp", "area_ha", "capa", "estado_evidencia"},
    "secciones": {"seccion", "tipo", "area_ha", "capa", "estado_evidencia"},
}


def iter_positions(coordinates: Any) -> Iterable[tuple[float, float]]:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/pdl_demo"))
    return parser.parse_args()


def main() -> int:
    data_dir = parse_args().data_dir.resolve()
    manifest_path = data_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0"
    assert manifest["crs"] == "EPSG:4326"
    assert manifest["population"]["population_sum"] == 79282
    assert manifest["privacy"] == {
        "personal_records": False,
        "absolute_source_paths": False,
        "property_whitelist_enforced": True,
    }

    layers = {item["id"]: item for item in manifest["layers"]}
    assert set(layers) == set(EXPECTED_COUNTS)
    assert sum(item["features"] for item in layers.values()) == 78

    for layer_id, expected_count in EXPECTED_COUNTS.items():
        entry = layers[layer_id]
        payload = json.loads((data_dir / entry["file"]).read_text(encoding="utf-8"))
        features = payload["features"]
        assert len(features) == expected_count
        assert entry["features"] == expected_count
        assert entry["unmatched_population_labels"] == []
        for feature in features:
            properties = set((feature.get("properties") or {}).keys())
            assert properties <= ALLOWED_PROPERTIES[layer_id], (
                layer_id,
                sorted(properties - ALLOWED_PROPERTIES[layer_id]),
            )
            positions = list(iter_positions(feature["geometry"]["coordinates"]))
            assert positions
            assert all(-180 <= lon <= 180 and -90 <= lat <= 90 for lon, lat in positions)

    locality_payload = json.loads(
        (data_dir / layers["localidades"]["file"]).read_text(encoding="utf-8")
    )
    assert all(
        int(feature["properties"].get("poblacion_total", 0)) >= 0
        for feature in locality_payload["features"]
    )
    assert all(
        feature["properties"].get("fuente_poblacion")
        for feature in locality_payload["features"]
    )
    print("PDL demo verified: 4 layers, 78 geometries, privacy whitelist clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
