"""CO•RA Conversation Tracker.

Rastrea conversaciones por identidad y localizador sin cargar todo el contenido
al contexto activo. Soporta índices versionados y archivos subidos en Streamlit.
"""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _fecha_iso(valor: Any) -> str | None:
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        try:
            return datetime.fromtimestamp(
                valor, tz=timezone.utc
            ).isoformat().replace("+00:00", "Z")
        except (ValueError, OSError, OverflowError):
            return None
    texto = str(valor).strip()
    return texto or None


def _hash_bytes(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def _slug_id(fuente: str, identidad: str) -> str:
    digest = hashlib.sha256(
        f"{fuente}|{identidad}".encode("utf-8")
    ).hexdigest()[:16]
    return f"{fuente}-{digest}"


def crear_registro(
    *,
    titulo: str,
    fuente: str,
    agente: str,
    identidad_origen: str,
    fecha: str | None = None,
    proyecto: str | None = None,
    hash_contenido: str | None = None,
    locator: dict | None = None,
) -> dict:
    titulo_limpio = (titulo or "Sin título").strip() or "Sin título"
    cid = _slug_id(fuente, identidad_origen or titulo_limpio)
    fecha_final = fecha or _ahora_iso()

    return {
        "id": cid,
        "conversation_id": cid,
        "titulo": titulo_limpio,
        "fuente": fuente,
        "fecha": fecha_final,
        "agente": agente,
        "proyecto": proyecto,
        "hash": hash_contenido,
        "locator": locator or {},
        "tracking_status": "indexed",
        "created_at": fecha_final,
        "updated_at": fecha_final,
        "agent": {
            "agent_id": fuente,
            "display_name": agente,
            "source_type": fuente,
            "model": None,
        },
        "context": {
            "project_id": None,
            "project_name": proyecto,
            "area_id": None,
            "objective": None,
        },
        "messages": [],
        "status": "indexed",
        "is_pinned": False,
        "categoria": "sin_clasificar",
        "fecha_extraccion": _ahora_iso(),
    }


def indice_a_conversacion(registro: dict) -> dict:
    fuente = registro.get("fuente") or "desconocido"
    agente = registro.get("agente") or fuente.title()
    identidad = (
        registro.get("id")
        or registro.get("conversation_id")
        or registro.get("titulo")
        or "sin-id"
    )

    base = crear_registro(
        titulo=registro.get("titulo") or registro.get("title") or "Sin título",
        fuente=fuente,
        agente=agente,
        identidad_origen=str(identidad),
        fecha=_fecha_iso(registro.get("fecha") or registro.get("created_at")),
        proyecto=registro.get("proyecto"),
        hash_contenido=registro.get("hash"),
        locator=registro.get("locator") or {
            "tipo": "indice",
            "archivo": registro.get("archivo_origen"),
            "conversation_id": (
                registro.get("id") or registro.get("conversation_id")
            ),
        },
    )

    if registro.get("conversation_id"):
        base["conversation_id"] = registro["conversation_id"]
    elif registro.get("id"):
        base["conversation_id"] = registro["id"]

    base["id"] = base["conversation_id"]
    return base


def cargar_indice_como_conversaciones(
    ruta: str = "data/conversaciones_indice.json",
) -> dict[str, dict]:
    path = Path(ruta)
    if not path.exists():
        return {}

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    salida: dict[str, dict] = {}

    for registro in payload.get("conversaciones", []):
        conv = indice_a_conversacion(registro)
        salida[conv["conversation_id"]] = conv

    return salida


def fusionar_conversaciones_session(
    actuales: dict[str, dict] | None,
    importadas: list[dict] | None = None,
    ruta_indice: str = "data/conversaciones_indice.json",
) -> dict[str, dict]:
    salida = cargar_indice_como_conversaciones(ruta_indice)

    for cid, conv in (actuales or {}).items():
        salida[cid] = conv

    for registro in importadas or []:
        conv = (
            registro
            if registro.get("conversation_id")
            else indice_a_conversacion(registro)
        )
        salida[conv["conversation_id"]] = conv

    return salida


def _extraer_chatgpt(data: list, archivo: str) -> list[dict]:
    resultados = []

    for indice, conv in enumerate(data):
        if not isinstance(conv, dict):
            continue

        original_id = str(
            conv.get("id")
            or conv.get("conversation_id")
            or f"{archivo}:{indice}"
        )

        titulo = (
            conv.get("title")
            or conv.get("titulo")
            or f"Conversación {indice + 1}"
        )

        fecha = _fecha_iso(
            conv.get("update_time") or conv.get("create_time")
        )

        fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "id": original_id,
                    "title": titulo,
                    "create_time": conv.get("create_time"),
                    "update_time": conv.get("update_time"),
                },
                sort_keys=True,
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()

        resultados.append(
            crear_registro(
                titulo=titulo,
                fuente="chatgpt",
                agente="ChatGPT",
                identidad_origen=original_id,
                fecha=fecha,
                hash_contenido=fingerprint,
                locator={
                    "tipo": "chatgpt_export",
                    "archivo": archivo,
                    "conversation_id": original_id,
                },
            )
        )

    return resultados


def _procesar_bytes(nombre: str, datos: bytes) -> list[dict]:
    ext = Path(nombre).suffix.lower()

    if ext == ".zip":
        salida: list[dict] = []

        with zipfile.ZipFile(io.BytesIO(datos)) as zf:
            for miembro in zf.namelist():
                if miembro.endswith("/"):
                    continue

                if Path(miembro).suffix.lower() not in {
                    ".json", ".jsonl", ".txt", ".md"
                }:
                    continue

                try:
                    salida.extend(
                        _procesar_bytes(miembro, zf.read(miembro))
                    )
                except (
                    KeyError,
                    UnicodeDecodeError,
                    json.JSONDecodeError,
                    zipfile.BadZipFile,
                ):
                    continue

        return salida

    if ext in {".txt", ".md"}:
        digest = _hash_bytes(datos)
        return [
            crear_registro(
                titulo=Path(nombre).stem,
                fuente=ext.lstrip("."),
                agente="Importado",
                identidad_origen=f"{nombre}:{digest}",
                hash_contenido=digest,
                locator={
                    "tipo": "archivo_subido",
                    "archivo": nombre,
                },
            )
        ]

    texto = datos.decode("utf-8", errors="ignore")

    if ext == ".jsonl":
        salida = []

        for numero, linea in enumerate(
            texto.splitlines(), start=1
        ):
            if not linea.strip():
                continue

            try:
                item = json.loads(linea)
            except json.JSONDecodeError:
                continue

            titulo = (
                item.get("titulo")
                or item.get("title")
                or f"{Path(nombre).stem} · {numero}"
            )

            salida.append(
                crear_registro(
                    titulo=titulo,
                    fuente=item.get("fuente") or "jsonl",
                    agente=item.get("agente") or "Importado",
                    identidad_origen=str(
                        item.get("id")
                        or item.get("conversation_id")
                        or f"{nombre}:{numero}"
                    ),
                    fecha=_fecha_iso(
                        item.get("fecha")
                        or item.get("created_at")
                    ),
                    proyecto=item.get("proyecto"),
                    hash_contenido=_hash_bytes(
                        linea.encode("utf-8")
                    ),
                    locator={
                        "tipo": "jsonl",
                        "archivo": nombre,
                        "linea": numero,
                    },
                )
            )

        return salida

    if ext == ".json":
        data = json.loads(texto)

        if isinstance(data, list):
            return _extraer_chatgpt(data, nombre)

        if isinstance(data, dict) and isinstance(
            data.get("conversaciones"), list
        ):
            return [
                indice_a_conversacion(item)
                for item in data["conversaciones"]
            ]

        if isinstance(data, dict):
            titulo = (
                data.get("titulo")
                or data.get("title")
                or Path(nombre).stem
            )

            fuente = (
                data.get("fuente")
                or data.get("agent", {}).get("source_type")
                or "json"
            )

            agente = (
                data.get("agente")
                or data.get("agent", {}).get("display_name")
                or "Importado"
            )

            original_id = str(
                data.get("id")
                or data.get("conversation_id")
                or nombre
            )

            return [
                crear_registro(
                    titulo=titulo,
                    fuente=fuente,
                    agente=agente,
                    identidad_origen=original_id,
                    fecha=_fecha_iso(
                        data.get("fecha")
                        or data.get("updated_at")
                        or data.get("created_at")
                    ),
                    proyecto=(
                        data.get("proyecto")
                        or data.get("context", {}).get(
                            "project_name"
                        )
                    ),
                    hash_contenido=_hash_bytes(datos),
                    locator={
                        "tipo": "json",
                        "archivo": nombre,
                        "conversation_id": original_id,
                    },
                )
            ]

    return []


def procesar_archivo_conversaciones(archivo) -> list[dict]:
    nombre = getattr(archivo, "name", "archivo")
    datos = archivo.getvalue()

    try:
        return _procesar_bytes(nombre, datos)
    except (
        json.JSONDecodeError,
        zipfile.BadZipFile,
        OSError,
        ValueError,
    ):
        return []


def exportar_indice(
    conversaciones: dict[str, dict] | list[dict],
) -> dict:
    valores = (
        conversaciones.values()
        if isinstance(conversaciones, dict)
        else conversaciones
    )

    indice = []

    for conv in valores:
        indice.append({
            "id": conv.get("conversation_id") or conv.get("id"),
            "titulo": conv.get("titulo") or "Sin título",
            "fuente": (
                conv.get("fuente")
                or conv.get("agent", {}).get("source_type")
            ),
            "fecha": (
                conv.get("updated_at")
                or conv.get("fecha")
            ),
            "agente": (
                conv.get("agente")
                or conv.get("agent", {}).get("display_name")
            ),
            "proyecto": (
                conv.get("proyecto")
                or conv.get("context", {}).get("project_name")
            ),
            "hash": conv.get("hash"),
            "locator": conv.get("locator") or {},
        })

    indice.sort(
        key=lambda x: x.get("fecha") or "",
        reverse=True,
    )

    return {
        "schema_version": "1.0",
        "actualizado": _ahora_iso(),
        "conversaciones": indice,
    }
