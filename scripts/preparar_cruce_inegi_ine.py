"""Genera un cruce territorial agregado INEGI-INE para el piloto PDL.

La relación se deriva exclusivamente de intersecciones entre polígonos. No
asigna habitantes, electores, domicilios ni resultados a una sección.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from shapely.geometry import shape


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/pdl_demo"))
    return parser.parse_args()


def load_geojson(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    data_dir = parse_args().data_dir.resolve()
    localities = load_geojson(data_dir / "localidades_poblacion.geojson")["features"]
    sections = load_geojson(data_dir / "secciones_46.geojson")["features"]
    section_geometries = [
        (feature["properties"], shape(feature["geometry"])) for feature in sections
    ]

    links: list[dict[str, Any]] = []
    for locality in localities:
        locality_properties = locality["properties"]
        locality_geometry = shape(locality["geometry"])
        intersections: list[tuple[float, str, str]] = []
        for section_properties, section_geometry in section_geometries:
            overlap = locality_geometry.intersection(section_geometry)
            if not overlap.is_empty and overlap.area > 1e-12:
                intersections.append(
                    (
                        float(overlap.area),
                        str(section_properties["seccion"]),
                        str(section_properties["tipo"]),
                    )
                )
        intersections.sort(reverse=True)
        links.append(
            {
                "localidad": locality_properties["nombre"],
                "poblacion_localidad": locality_properties.get("poblacion_total", 0),
                "fuente_poblacion": locality_properties.get("fuente_poblacion", ""),
                "secciones_intersectadas": [item[1] for item in intersections],
                "cantidad_secciones": len(intersections),
                "seccion_mayor_interseccion": intersections[0][1] if intersections else None,
                "tipos_seccion": sorted({item[2] for item in intersections}),
                "metodo": "interseccion_geometrica; orden por mayor superficie compartida",
            }
        )

    type_counts = Counter(str(item["properties"]["tipo"]) for item in sections)
    payload = {
        "schema_version": "1.0",
        "municipio": {
            "nombre": "Tejupilco",
            "cvegeo_inegi": "15082",
            "cve_ent": "15",
            "cve_mun": "082",
            "referencia": "INEGI, Catálogo Único de Claves Geoestadísticas",
            "referencia_url": "https://www.inegi.org.mx/servicios/catalogounico.html",
        },
        "marco_electoral": {
            "institucion": "INE",
            "secciones_en_capa_local": len(sections),
            "tipos": dict(sorted(type_counts.items())),
            "referencia": "INE, SIGE 8 y descriptivo de distritación electoral",
            "referencia_url": "https://cartografia.ine.mx/sige8/",
            "corroboracion_46_secciones_url": (
                "https://repositoriodocumental.ine.mx/xmlui/bitstream/handle/"
                "123456789/141325/CGex202208-22-ap-1-1-a3b.pdf"
            ),
            "estado": "cantidad corroborada; corte y localizador exacto de la geometria local pendientes",
        },
        "crosswalk": links,
        "methodology": {
            "relation": "localidad_poligono intersecta seccion_poligono",
            "crs": "EPSG:4326 para la prueba topologica",
            "dominant_rule": "seccion con mayor superficie compartida en la capa común",
            "population_assignment": False,
            "individual_records": False,
            "warning": (
                "La población pertenece a la localidad agregada. No representa padrón, "
                "lista nominal, intención de voto ni habitantes asignados a una sección."
            ),
        },
    }
    write_json(data_dir / "cruce_inegi_ine.json", payload)
    print(
        f"INEGI-INE crosswalk prepared: {len(links)} localities, "
        f"{len(sections)} electoral sections."
    )
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
