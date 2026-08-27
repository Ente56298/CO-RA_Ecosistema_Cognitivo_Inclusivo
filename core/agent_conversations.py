"""
CO•RA — Conversaciones con Agentes
MVP 1: formato común + conversación en memoria de sesión + exportación JSON.

No llama APIs ni modelos por sí mismo.
Sirve como capa común para Qwen, ChatGPT, gpt-oss, Gemini u otros agentes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def _ahora_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def nueva_conversacion(
    agent_id: str,
    agent_name: str,
    project_id: str | None = None,
    project_name: str | None = None,
    area_id: str | None = None,
    objective: str | None = None,
    source_type: str = "manual",
    model: str | None = None,
) -> dict:
    """Crea el contenedor canónico de una conversación CO•RA."""
    return {
        "schema_version": "1.0",
        "conversation_id": f"conv-{uuid4().hex[:12]}",
        "created_at": _ahora_iso(),
        "updated_at": _ahora_iso(),
        "agent": {
            "agent_id": agent_id,
            "display_name": agent_name,
            "source_type": source_type,
            "model": model,
        },
        "context": {
            "project_id": project_id,
            "project_name": project_name,
            "area_id": area_id,
            "objective": objective,
        },
        "messages": [],
        "status": "active",
    }


def agregar_mensaje(
    conversation: dict,
    role: str,
    content: str,
    author: str | None = None,
    metadata: dict | None = None,
) -> dict:
    """Agrega un mensaje sin mutar la semántica del historial."""
    texto = (content or "").strip()
    if not texto:
        return conversation

    conversation.setdefault("messages", []).append(
        {
            "message_id": f"msg-{uuid4().hex[:12]}",
            "timestamp": _ahora_iso(),
            "role": role,
            "author": author,
            "content": texto,
            "metadata": metadata or {},
        }
    )
    conversation["updated_at"] = _ahora_iso()
    return conversation


def resumen_para_mesa(conversation: dict) -> dict:
    """
    Prepara un artefacto para la Mesa Redonda.
    No inventa una síntesis: conserva mensajes y deja la síntesis pendiente.
    """
    mensajes = conversation.get("messages", [])
    return {
        "tipo": "entrada_mesa_redonda",
        "conversation_id": conversation.get("conversation_id"),
        "agent": conversation.get("agent", {}),
        "context": conversation.get("context", {}),
        "message_count": len(mensajes),
        "messages": mensajes,
        "sintesis": None,
        "estado": "pendiente_revision_humana",
        "prepared_at": _ahora_iso(),
    }
