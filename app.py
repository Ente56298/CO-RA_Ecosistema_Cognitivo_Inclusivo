"""
CO•RA Tutor — Trayectoria Adaptativa de Aprendizaje
Versión 2.2: Mapa de avances + Mapa abierto + Rastreo de contextos + GitHub Bridge
"""
import streamlit as st
import pydeck as pdk
import requests
import json
import hashlib
import base64
import io
import math
import struct
import time
import wave
from datetime import datetime, timezone
from pathlib import Path


from core.conversation_tracker import (
    cargar_indice_como_conversaciones,
    exportar_indice,
    fusionar_conversaciones_session,
    procesar_archivo_conversaciones,
)

BASE_DIR = Path(__file__).resolve().parent
INDICE_CONVERSACIONES = BASE_DIR / "data" / "conversaciones_indice.json"



# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="CO•RA Tutor",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURACIÓN GITHUB
# ============================================
try:
    GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
    ENABLE_GITHUB_WRITES = st.secrets.get("ENABLE_GITHUB_WRITES", False)
except st.errors.StreamlitSecretNotFoundError:
    GITHUB_TOKEN = ""
    ENABLE_GITHUB_WRITES = False
GITHUB_USER = "Ente56298"
REPO_NAME = "CO-RA_Ecosistema_Cognitivo_Inclusivo"

# ============================================
# ÁREAS DE CONOCIMIENTO (accesos frecuentes, no límites)
# ============================================
AREAS_CONOCIMIENTO = {
    'redes': {
        'nombre': 'Redes y Direccionamiento',
        'icono': '🌐',
        'descripcion': 'IP, DNS, protocolos, infraestructura de red',
        'pregunta': '¿Qué es una dirección IP y para qué sirve?',
        'palabras_clave': ['ip', 'red', 'dns', 'router', 'protocolo', 'tcp', 'udp'],
        'conectadas': ['programacion', 'geoespacial']
    },
    'programacion': {
        'nombre': 'Programación y Automatización',
        'icono': '💻',
        'descripcion': 'Python, Excel VBA, APIs, scripts, automatización',
        'pregunta': '¿Qué es una API y cómo permite la comunicación entre sistemas?',
        'palabras_clave': ['python', 'excel', 'vba', 'macro', 'script', 'api', 'código', 'automat'],
        'conectadas': ['redes', 'ia', 'desarrollo_web', 'contable']
    },
    'contable': {
        'nombre': 'Contabilidad y Fiscal (SAT/NIF)',
        'icono': '📊',
        'descripcion': 'Agrupadores SAT, NIF, catálogo de cuentas, fiscal mexicano',
        'pregunta': '¿Qué es un agrupador SAT y cómo se relaciona con las NIF?',
        'palabras_clave': ['sat', 'nif', 'agrupador', 'cuenta', 'activo', 'fiscal', 'contab', 'catálogo'],
        'conectadas': ['programacion', 'municipal']
    },
    'municipal': {
        'nombre': 'Gestión Municipal y Transparencia',
        'icono': '🏛️',
        'descripcion': 'PDM, PAE, transparencia, SAIMEX, gobierno municipal',
        'pregunta': '¿Qué es el PDM y cómo se evalúa su cumplimiento?',
        'palabras_clave': ['pdm', 'pai', 'transparencia', 'saimes', 'municipal', 'tejupilco', 'icati', 'ayuntamiento'],
        'conectadas': ['evaluacion', 'contable', 'geoespacial']
    },
    'geoespacial': {
        'nombre': 'Sistemas de Información Geográfica',
        'icono': '🗺️',
        'descripcion': 'QGIS, shapefiles, KMZ, cartografía, georreferenciación',
        'pregunta': '¿Qué es un shapefile y para qué se usa en análisis territorial?',
        'palabras_clave': ['qgis', 'shapefile', 'kmz', 'mapa', 'gis', 'coordenadas', 'geoespacial', 'cartografía'],
        'conectadas': ['municipal', 'redes', 'evaluacion']
    },
    'ia': {
        'nombre': 'Inteligencia Artificial',
        'icono': '🤖',
        'descripcion': 'IA, LLM, automatización inteligente, agentes',
        'pregunta': '¿Cómo aprende un modelo de IA a partir de datos?',
        'palabras_clave': ['ia', 'inteligencia artificial', 'gpt', 'chatgpt', 'modelo', 'prompt', 'agente', 'machine learning'],
        'conectadas': ['programacion', 'desarrollo_web']
    },
    'evaluacion': {
        'nombre': 'Evaluación de Programas',
        'icono': '📈',
        'descripcion': 'PbR, MIR, indicadores, evaluación de desempeño',
        'pregunta': '¿Qué es la Metodología de Marco Lógico (MIR)?',
        'palabras_clave': ['evaluación', 'indicador', 'mir', 'pbr', 'programa', 'meta', 'pae'],
        'conectadas': ['municipal', 'contable']
    },
    'desarrollo_web': {
        'nombre': 'Desarrollo Web',
        'icono': '🌍',
        'descripcion': 'HTML, CSS, JavaScript, Streamlit, aplicaciones interactivas',
        'pregunta': '¿Cómo se estructura una página web básica?',
        'palabras_clave': ['html', 'css', 'javascript', 'streamlit', 'web', 'app', 'frontend', 'backend'],
        'conectadas': ['programacion', 'ia']
    },
    'oportunidades': {
        'nombre': 'Oportunidades e Ingresos',
        'icono': '💼',
        'descripcion': 'Trabajo, convocatorias, servicios, financiamiento y sostenibilidad de proyectos',
        'pregunta': '¿Qué oportunidad puede convertirse en un ingreso verificable y sostenible?',
        'palabras_clave': [
            'trabajo', 'vacante', 'oportunidad', 'ingreso', 'freelance', 'workana',
            'convocatoria', 'financiamiento', 'propuesta', 'cliente', 'servicio'
        ],
        'conectadas': ['ia', 'programacion', 'municipal', 'evaluacion']
    },
    'mapa_abierto': {
        'nombre': 'Mapa Abierto de Conocimiento',
        'icono': '🧭',
        'descripcion': 'Exploración interdisciplinaria sin una categoría previa obligatoria',
        'pregunta': '¿Qué observas y con qué ideas podría relacionarse?',
        'palabras_clave': [],
        'conectadas': []
    }
}

# ============================================
# CLASE PUENTE GITHUB
# ============================================
class CORAGitHubBridge:
    """Puente de integración entre Streamlit y GitHub Memory Bank"""
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def leer_contexto(self, ruta: str):
        """Recupera contexto desde GitHub Memory Bank"""
        try:
            url = f"{self.base_url}/{ruta}"
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                content = base64.b64decode(response.json()["content"]).decode('utf-8')
                if ruta.endswith(".jsonl"):
                    return [json.loads(line) for line in content.splitlines() if line.strip()]
                return json.loads(content)
        except Exception as e:
            st.error(f"Error leyendo contexto: {e}")
        return None
    
    def anclar_evento(self, usuario: str, evento_id: str, payload: dict):
        """Ancla evento en Matriz Dorsal con hash SHA-512"""
        if not ENABLE_GITHUB_WRITES:
            st.warning("La escritura pública está desactivada. Descarga el evento para revisarlo localmente.")
            return None
        try:
            ruta = f"matriz_dorsal/usuarios/{usuario}/eventos.jsonl"
            url = f"{self.base_url}/{ruta}"
            
            response = requests.get(url, headers=self.headers, timeout=15)
            contenido_actual = ""
            sha_actual = ""
            
            if response.status_code == 200:
                contenido_actual = base64.b64decode(response.json()["content"]).decode('utf-8')
                sha_actual = response.json()["sha"]
            
            payload_str = json.dumps(payload, sort_keys=True)
            hash_forense = hashlib.sha512(payload_str.encode('utf-8')).hexdigest()
            
            nuevo_registro = {
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "evento_id": evento_id,
                "usuario": usuario,
                "hash_sha512": hash_forense,
                "datos": payload
            }
            
            contenido_nuevo = contenido_actual + json.dumps(nuevo_registro) + "\n"
            
            commit_data = {
                "message": f"🔒 [CO•RA] {evento_id} | {usuario}",
                "content": base64.b64encode(contenido_nuevo.encode('utf-8')).decode('utf-8'),
                "branch": "main"
            }
            if sha_actual:
                commit_data["sha"] = sha_actual
            
            return requests.put(url, headers=self.headers, json=commit_data, timeout=20)
        except Exception as e:
            st.error(f"Error anclando evento: {e}")
            return None

# ============================================
# RASTREADOR DE CONTEXTOS
# ============================================
def rastrear_contextos_previos(area_id: str, historial: list) -> list:
    """Rastrea conversaciones previas relacionadas con un área"""
    area = AREAS_CONOCIMIENTO.get(area_id, {})
    palabras_clave = area.get('palabras_clave', [])
    contextos_encontrados = []
    
    for conv in historial:
        titulo = conv.get('titulo', '').lower()
        coincidencias = sum(1 for palabra in palabras_clave if palabra in titulo)
        
        if coincidencias > 0:
            relevancia = coincidencias / len(palabras_clave)
            contextos_encontrados.append({
                'titulo': conv.get('titulo', ''),
                'relevancia': relevancia,
                'is_pinned': conv.get('is_pinned', False),
                'coincidencias': coincidencias
            })
    
    return sorted(contextos_encontrados, key=lambda x: x['relevancia'], reverse=True)

def generar_recomendacion(area_nombre: str, contextos: list) -> str:
    """Genera recomendación personalizada basada en contextos previos"""
    if len(contextos) == 0:
        return f"🌱 Esta es tu primera exploración de {area_nombre}. Empezaremos desde los fundamentos."
    elif len(contextos) <= 2:
        return f"🌱 Ya exploraste '{contextos[0]['titulo'][:50]}...'. Podemos construir sobre esa base."
    elif len(contextos) <= 5:
        return f"📚 Tienes {len(contextos)} conversaciones previas en esta área. Nivel intermedio detectado."
    else:
        return f"🎯 Eres usuario avanzado en {area_nombre} ({len(contextos)} contextos). Podemos ir directo a casos complejos."

# ============================================
# CARGAR DATOS
# ============================================
def cargar_conversaciones():
    """Carga metadatos desde el índice canónico, nunca contenido privado."""
    return list(
        cargar_indice_como_conversaciones(str(INDICE_CONVERSACIONES)).values()
    )


def cargar_json_publico(ruta: str, valor_por_defecto):
    """Carga un artefacto público versionado sin exponer datos locales."""
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return valor_por_defecto


def to_simple_table(rows, columns):
    """Convierte una lista de dicts en una tabla plana para Streamlit."""
    return [
        {column: row.get(column, "") for column in columns}
        for row in rows
    ]


@st.cache_data
def generar_senal_foco(frecuencias=(660, 880), duracion=0.16, volumen=0.20):
    """Genera una señal WAV breve sin depender de archivos ni servicios externos."""
    sample_rate = 22050
    frames = bytearray()
    for frecuencia in frecuencias:
        total = int(sample_rate * duracion)
        for indice in range(total):
            envolvente = min(1.0, indice / max(total * 0.08, 1))
            envolvente *= min(1.0, (total - indice) / max(total * 0.18, 1))
            muestra = volumen * envolvente * math.sin(
                2 * math.pi * frecuencia * indice / sample_rate
            )
            frames.extend(struct.pack("<h", int(32767 * muestra)))

    salida = io.BytesIO()
    with wave.open(salida, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(bytes(frames))
    return salida.getvalue()


@st.fragment(run_every=1)
def render_widget_foco(actividades):
    """Widget de foco persistente durante la sesión y visible en toda la app."""
    candidatas = [
        item for item in actividades
        if item.get("state") not in {"completada", "bloqueada"}
    ] or actividades

    with st.container(border=True):
        st.markdown("### 🎯 Foco activo")
        st.caption("Una actividad. Un bloque. Un siguiente paso.")

        if not candidatas:
            st.info("No hay actividades disponibles para enfocar.")
            return

        ids = [item.get("id", "") for item in candidatas]
        por_id = {item.get("id", ""): item for item in candidatas}
        seleccion = st.selectbox(
            "Actividad actual",
            ids,
            index=next(
                (
                    indice for indice, item in enumerate(candidatas)
                    if item.get("focus_default")
                ),
                0,
            ),
            format_func=lambda activity_id: por_id.get(activity_id, {}).get(
                "title", activity_id
            ),
            key="foco_actividad_id",
        )
        actividad = por_id.get(seleccion, {})
        st.caption(
            f"{actividad.get('project', 'Sin proyecto')} · "
            f"Prioridad {actividad.get('priority', 'sin prioridad')}"
        )
        st.write("**Ahora:** " + actividad.get("next_action", "Sin siguiente acción."))

        duracion = st.select_slider(
            "Duración del bloque",
            options=[5, 10, 15, 25, 45],
            value=15,
            format_func=lambda minutos: f"{minutos} min",
            key="foco_duracion_minutos",
        )
        audio_activo = st.toggle(
            "Señales de audio",
            value=False,
            key="foco_audio_activo",
            help="Sonido breve al iniciar y terminar. Puede requerir interacción con el navegador.",
        )

        if "foco_activo" not in st.session_state:
            st.session_state.foco_activo = False
        if "foco_checkins" not in st.session_state:
            st.session_state.foco_checkins = 0
        if "foco_fin_emitido" not in st.session_state:
            st.session_state.foco_fin_emitido = False

        iniciar, detener = st.columns(2)
        with iniciar:
            if st.button("▶️ Iniciar", use_container_width=True, key="foco_iniciar"):
                ahora = time.time()
                st.session_state.foco_activo = True
                st.session_state.foco_inicio_epoch = ahora
                st.session_state.foco_fin_epoch = ahora + duracion * 60
                st.session_state.foco_duracion_segundos = duracion * 60
                st.session_state.foco_fin_emitido = False
                if audio_activo:
                    st.audio(generar_senal_foco(), format="audio/wav", autoplay=True)
        with detener:
            if st.button("⏹️ Detener", use_container_width=True, key="foco_detener"):
                st.session_state.foco_activo = False

        if st.session_state.get("foco_activo"):
            ahora = time.time()
            restante = max(0, int(st.session_state.get("foco_fin_epoch", ahora) - ahora))
            total = max(1, int(st.session_state.get("foco_duracion_segundos", 1)))
            transcurrido = total - restante
            minutos, segundos = divmod(restante, 60)
            st.metric("Tiempo restante", f"{minutos:02d}:{segundos:02d}")
            st.progress(min(1.0, max(0.0, transcurrido / total)))

            if restante <= 0:
                st.session_state.foco_activo = False
                st.success("Bloque terminado. Respira y registra el avance.")
                if audio_activo and not st.session_state.foco_fin_emitido:
                    st.session_state.foco_fin_emitido = True
                    st.audio(generar_senal_foco((880, 1040)), format="audio/wav", autoplay=True)
        else:
            st.progress(0)

        sigo, cerrar, cambiar = st.columns(3)
        with sigo:
            if st.button("👁️ Sigo", key="foco_sigo", help="Registra un retorno amable al foco."):
                st.session_state.foco_checkins += 1
                st.toast("Aquí seguimos. Retoma sólo el siguiente paso.")
        with cerrar:
            if st.button("✅ Cerrar", key="foco_cerrar", help="Cierra este bloque, no toda la actividad."):
                st.session_state.foco_activo = False
                st.session_state.foco_ultimo_cierre = datetime.now(
                    timezone.utc
                ).isoformat().replace("+00:00", "Z")
                st.success("Bloque registrado en esta sesión.")
        with cambiar:
            if st.button("🔄 Cambiar", key="foco_cambiar", help="Detiene el bloque para elegir otra actividad."):
                st.session_state.foco_activo = False
                st.toast("Elige otra actividad sin perder la matriz.")

        st.caption(
            f"Retornos al foco en esta sesión: {st.session_state.foco_checkins}. "
            "No se publica este registro."
        )


@st.fragment(run_every=2)
def render_presentacion_inmersiva(
    proyectos,
    actividades,
    activos,
    trayectoria,
    indice_conversaciones,
):
    """Presentación interactiva en tiempo real con datos públicos y sanitizados."""
    proyectos_por_id = {
        item.get("id", ""): item for item in proyectos if item.get("id")
    }
    actividades_por_proyecto = {}
    for actividad in actividades:
        pid = actividad.get("project_id", "")
        actividades_por_proyecto.setdefault(pid, []).append(actividad)

    proyecto_ids = list(proyectos_por_id.keys())
    if not proyecto_ids:
        st.warning("No hay proyectos públicos cargados para la presentación.")
        return

    estado_general = {
        "en_desarrollo": sum(1 for item in proyectos if item.get("estado") == "en_desarrollo"),
        "prototipo": sum(1 for item in proyectos if item.get("estado") == "prototipo"),
        "operativo": sum(1 for item in proyectos if item.get("estado") == "operativo"),
    }
    actividades_activas = [
        item for item in actividades if item.get("state") in {"pendiente", "en_curso", "en_revision"}
    ]
    completadas = sum(1 for item in actividades if item.get("state") == "completada")
    foco_id = next(
        (item.get("id") for item in actividades if item.get("focus_default")),
        actividades_activas[0].get("id") if actividades_activas else actividades[0].get("id"),
    )

    st.markdown(
        """
        <style>
        .cora-stage {
            padding: 1.35rem 1.2rem;
            border-radius: 1.25rem;
            background:
                radial-gradient(circle at 15% 10%, rgba(121, 58, 242, 0.28), transparent 28%),
                radial-gradient(circle at 80% 15%, rgba(41, 182, 246, 0.22), transparent 26%),
                linear-gradient(135deg, #07101D 0%, #09192D 42%, #0C2340 100%);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 24px 60px rgba(0,0,0,0.35);
            color: white;
            margin-bottom: 1rem;
        }
        .cora-hero {
            padding: 1.1rem 1.15rem 1rem 1.15rem;
            border-radius: 1rem;
            background: linear-gradient(135deg, rgba(31,77,120,0.95) 0%, rgba(13,35,60,0.92) 100%);
            color: white;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .cora-hero h1, .cora-hero h2, .cora-hero p {
            color: white !important;
        }
        .cora-kicker {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.74rem;
            color: rgba(255,255,255,0.72);
            margin-bottom: 0.45rem;
        }
        .cora-chip {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            margin: 0.15rem 0.2rem 0.15rem 0;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            color: white;
            font-size: 0.82rem;
        }
        .cora-card {
            padding: 0.95rem 1rem;
            border-radius: 0.95rem;
            background: rgba(10, 20, 36, 0.82);
            border: 1px solid rgba(255,255,255,0.08);
            color: white;
            min-height: 100%;
        }
        .cora-card h3, .cora-card h4, .cora-card p, .cora-card div, .cora-card span {
            color: white !important;
        }
        .cora-badge {
            display: inline-block;
            padding: 0.18rem 0.5rem;
            border-radius: 999px;
            background: rgba(41,182,246,0.18);
            border: 1px solid rgba(41,182,246,0.25);
            color: #DDF4FF;
            font-size: 0.78rem;
            margin-right: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            """
            <div class="cora-stage">
              <div class="cora-kicker">CO•RA / PDL · PRESENTACION INMERSIVA</div>
              <div class="cora-hero">
                <h1>El futuro del proyecto, en tus manos</h1>
                <p>Explora datos reales, proyectos vivos, activos y trayectoria en una lectura territorial interactiva, clara y trazable.</p>
                <div>
                  <span class="cora-chip">Datos reales</span>
                  <span class="cora-chip">Relaciones vivas</span>
                  <span class="cora-chip">Trayectoria</span>
                  <span class="cora-chip">Activos</span>
                  <span class="cora-chip">Evidencia</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Proyectos", len(proyecto_ids))
        m2.metric("Actividades activas", len(actividades_activas))
        m3.metric("Completadas", completadas)
        m4.metric("Activos públicos", len(activos))
        m5.metric("Títulos indexados", len(indice_conversaciones))

        st.caption(
            "La presentación no reproduce contenido privado. Usa títulos, metadatos, estados y relaciones ya sanitizadas."
        )

        escena = st.radio(
            "Recorrido visual",
            [
                "Portada",
                "Proyectos vivos",
                "Actividad y foco",
                "Trayectoria",
                "Activos y conversaciones",
                "Cierre",
            ],
            horizontal=True,
            key="presentacion_escena",
        )

        col_left, col_right = st.columns([1.08, 0.92])
        with col_left:
            if escena in {"Portada", "Proyectos vivos", "Actividad y foco"}:
                seleccion = st.selectbox(
                    "Proyecto a explorar",
                    proyecto_ids,
                    index=proyecto_ids.index("radar-pdl") if "radar-pdl" in proyecto_ids else 0,
                    format_func=lambda pid: proyectos_por_id.get(pid, {}).get("nombre", pid),
                    key="presentacion_proyecto_id",
                )
            else:
                seleccion = st.session_state.get("presentacion_proyecto_id", "radar-pdl" if "radar-pdl" in proyecto_ids else proyecto_ids[0])
            proyecto = proyectos_por_id[seleccion]
            if escena == "Portada":
                st.markdown(
                    f"""
                    <div class="cora-card">
                      <h3>{proyecto.get('nombre', seleccion)}</h3>
                      <p>{proyecto.get('ahora', '')}</p>
                      <p><b>Siguiente:</b> {proyecto.get('siguiente', '')}</p>
                      <div>
                        <span class="cora-badge">Estado: {proyecto.get('estado', '')}</span>
                        <span class="cora-badge">Confianza: {proyecto.get('confianza', '')}</span>
                      </div>
                      <p style="margin-top:0.5rem;">Fuentes: {", ".join(proyecto.get('fuentes', []))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("#### Visión que se proyecta")
                st.write(
                    "Territorio, trayectoria, conversaciones, activos y actividades aparecen como capas conectadas."
                )
            elif escena == "Proyectos vivos":
                st.markdown("#### Mapa de proyectos")
                proyecto_tarjetas = st.columns(2)
                for idx, pid in enumerate(proyecto_ids[:4]):
                    p = proyectos_por_id[pid]
                    with proyecto_tarjetas[idx % 2]:
                        with st.container(border=True):
                            st.markdown(f"**{p.get('nombre', pid)}**")
                            st.caption(f"{p.get('estado', '')} · confianza {p.get('confianza', '')}")
                            st.write(p.get("ahora", ""))
                            st.write("**Siguiente:** " + p.get("siguiente", ""))
                            st.caption("Fuentes: " + ", ".join(p.get("fuentes", [])))
            elif escena == "Actividad y foco":
                st.markdown("#### Foco operativo")
                actividades_proyecto = actividades_por_proyecto.get(seleccion, [])
                if actividades_proyecto:
                    for item in sorted(actividades_proyecto, key=lambda x: (x.get("priority", "zzz"), x.get("id", ""))):
                        with st.container(border=True):
                            st.markdown(
                                f"**{item.get('title', 'Actividad')}** · "
                                f"{item.get('state', 'sin estado').replace('_', ' ')}"
                            )
                            st.caption(
                                f"Capa {item.get('layer', 0)} · Prioridad {item.get('priority', '')} · Avance {item.get('progress', 0)}%"
                            )
                            st.progress(int(item.get("progress", 0)) / 100)
                            st.write(item.get("next_action", ""))
                            st.write("**Evidencia:** " + item.get("completion_evidence", ""))
                else:
                    st.info("No hay actividades asociadas directamente a este proyecto.")
            elif escena == "Trayectoria":
                st.markdown("#### Respaldo de trayectoria")
                t1, t2, t3 = st.columns(3)
                with t1:
                    st.metric("Periodos", len(trayectoria.get("experience", [])))
                with t2:
                    st.metric("Dominios", len(trayectoria.get("capability_matrix", [])))
                with t3:
                    st.metric("Fuentes", len(trayectoria.get("source_layers", [])))
                st.dataframe(
                    [
                        {
                            "Periodo": item.get("period", ""),
                            "Ambito": item.get("scope", ""),
                            "Rol": item.get("role", ""),
                            "Nivel": item.get("level", ""),
                            "Estado": item.get("status", ""),
                        }
                        for item in trayectoria.get("experience", [])
                    ],
                    width="stretch",
                    hide_index=True,
                )
            elif escena == "Activos y conversaciones":
                st.markdown("#### Activos que sostienen la vision")
                activos_mostrados = cols = st.columns(3)
                for idx, item in enumerate(activos[:6]):
                    with activos_mostrados[idx % 3]:
                        with st.container(border=True):
                            st.markdown(f"**{item.get('name', '')}**")
                            st.caption(item.get("domain", "") + " · " + item.get("status", ""))
                            st.write(item.get("relation", ""))
                st.markdown("#### Títulos de conversaciones")
                for titulo in [
                    item.get("titulo", item.get("title", "Sin título"))
                    for item in indice_conversaciones[:10]
                ]:
                    st.write(f"- {titulo}")
            else:
                st.markdown("#### Cierre de vision")
                st.success("PDL convierte fragmentos dispersos en una lectura territorial trazable, viva y util para decidir.")
                st.write("vision -> proyecto -> actividad -> activo -> evidencia -> decision")
                st.write("Selecciona un proyecto para ver cómo cambia el sistema en vivo.")

        with col_right:
            st.markdown("#### Radar vivo")
            foco_actual = next(
                (item for item in actividades if item.get("id") == foco_id),
                actividades[0] if actividades else {},
            )
            with st.container(border=True):
                st.markdown(
                    f"**{foco_actual.get('title', 'Sin foco actual')}**  \n"
                    f"{foco_actual.get('project', 'Sin proyecto')} · "
                    f"Capa {foco_actual.get('layer', 0)} · "
                    f"{foco_actual.get('state', '').replace('_', ' ')}"
                )
                st.progress(int(foco_actual.get("progress", 0)) / 100 if foco_actual else 0)
                st.caption("Foco actual que sostiene el ritmo de avance.")
                st.write("**Siguiente acción:** " + foco_actual.get("next_action", ""))
                st.write("**Evidencia de cierre:** " + foco_actual.get("completion_evidence", ""))

            st.markdown("#### Una mirada al futuro")
            st.write(
                "La escena debe hacer sentir que el sistema ya está preparado para crecer: cada clic abre una capa, cada capa deja ver otra decisión."
            )
            future_cols = st.columns(2)
            with future_cols[0]:
                st.metric("Actividades en movimiento", len(actividades_activas))
            with future_cols[1]:
                st.metric("Vigencia de activos", len([a for a in activos if a.get("status") == "activo"]))

            st.markdown("#### Descarga pública")
            if st.button("Preparar instantanea", key="presentacion_snapshot_button"):
                st.toast("Instantánea lista para descarga.")
            st.download_button(
                "⬇️ Descargar fotografía pública JSON",
                data=json.dumps(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                        "project_selected": seleccion,
                        "project": proyecto,
                        "focus_activity": foco_actual,
                        "projects_count": len(proyectos),
                        "active_activities": len(actividades_activas),
                        "public_assets": len(activos),
                        "conversation_titles": [
                            item.get("titulo", item.get("title", "Sin título"))
                            for item in indice_conversaciones[:10]
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                file_name="cora_presentacion_inmersiva_snapshot.json",
                mime="application/json",
            )

# ============================================
# AMPLIAR ÁREAS DESDE CATÁLOGO EXTERNO
# ============================================
AREAS_EXTRA = cargar_json_publico(
    "data/areas_conocimiento.json",
    {}
)

AREAS_CONOCIMIENTO.update(AREAS_EXTRA)

PROYECTOS_PUBLICOS = cargar_json_publico(
    "data/proyectos_actuales.json",
    {"projects": []},
).get("projects", [])

ACTIVOS_PUBLICOS = cargar_json_publico(
    "data/catalogo_activos_publico.json",
    {"assets": []},
).get("assets", [])

TRAYECTORIA_PUBLICA = cargar_json_publico(
    "data/matriz_trayectoria_evidencias_publico.json",
    {},
)

INDICE_CONVERSACIONES_PUBLICO = cargar_conversaciones()

ACTIVIDADES_PUBLICAS = cargar_json_publico(
    "data/actividades_seguimiento.json",
    {"activities": []},
).get("activities", [])










# ============================================
# INTERFAZ PRINCIPAL
# ============================================
st.title("🧭 CO•RA Tutor")
st.markdown("### Trayectoria adaptativa de aprendizaje y conocimiento")
st.caption("Contexto abundante por detrás; simplicidad por delante.")

# Sidebar - Configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    usuario = st.text_input("Usuario", value="Jorge")
    token = GITHUB_TOKEN
    bridge = CORAGitHubBridge(token, GITHUB_USER, REPO_NAME)

    if token:
        st.success("✅ Memory Bank configurado por el servidor")
    else:
        st.info("ℹ️ Catálogo y mesa disponibles en modo público")
    
    st.markdown("---")
    st.subheader("🔧 Motores Activos")
    st.write("✅ Mapa de avances")
    st.write("✅ Rastreo de contextos")
    st.write("✅ Mapa abierto de conocimiento")
    st.write("✅ Radar de oportunidades e ingresos")
    st.write("✅ Catálogo público de agentes")
    st.write("✅ Mesa redonda colaborativa")
    st.write("⚠️ Escritura en Memory Bank desactivada" if not ENABLE_GITHUB_WRITES else "✅ Escritura privada habilitada")

    st.markdown("---")
    actividades_foco = cargar_json_publico(
        "data/actividades_seguimiento.json",
        {"activities": []},
    ).get("activities", [])
    render_widget_foco(actividades_foco)

# Tabs principales
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🎯 Trayectoria y proyectos",
    "📚 Conversaciones y registros",
    "🧠 Memoria y contexto",
    "🤝 Agentes y evaluación",
    "🧩 Plantillas y referencias",
    "🗃️ Activos y recursos",
    "💬 Mesa colaborativa",
    "✅ Seguimiento de actividades",
    "🎞️ Presentación inmersiva",
    "🧮 Analizador maestro"
])

# ============================================
# TAB 1: EXPLORAR ÁREA
# ============================================
with tab1:
    # ============================================
    # MAPA DE AVANCES
    # ============================================
    st.subheader("🗺️ Mapa de Avances")
    st.caption(
        "Proyectos vivos inferidos desde conversaciones, código, memoria, "
        "documentos e inventarios contextuales. Los estados representan "
        "evidencia de continuidad; no son una calificación."
    )

    mapa_proyectos = cargar_json_publico(
        "data/proyectos_actuales.json",
        {"actualizado": None, "proyectos": []},
    )
    proyectos = mapa_proyectos.get("proyectos", [])

    iconos_estado = {
        "idea": "⚪",
        "exploracion": "🔵",
        "prototipo": "🟣",
        "en_desarrollo": "🟡",
        "bloqueado": "🟠",
        "operativo": "🟢",
        "consolidado": "✅",
        "archivado": "⚫",
    }

    if proyectos:
        actualizado = mapa_proyectos.get("actualizado")
        if actualizado:
            st.caption(f"Última actualización: {actualizado}")
        if mapa_proyectos.get("metodo"):
            st.info(mapa_proyectos["metodo"])

        total_proyectos = len(proyectos)
        operativos = sum(1 for p in proyectos if p.get("estado") == "operativo")
        en_desarrollo = sum(1 for p in proyectos if p.get("estado") == "en_desarrollo")
        bloqueados = sum(1 for p in proyectos if p.get("estado") == "bloqueado")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Proyectos", total_proyectos)
        col_m2.metric("Operativos", operativos)
        col_m3.metric("En desarrollo", en_desarrollo)
        col_m4.metric("Bloqueados", bloqueados)

        st.markdown("")
        columnas_proyectos = st.columns(2)

        for indice, proyecto in enumerate(proyectos):
            estado = proyecto.get("estado", "idea")
            icono = iconos_estado.get(estado, "⚪")

            with columnas_proyectos[indice % 2]:
                with st.container(border=True):
                    st.markdown(
                        f"### {icono} {proyecto.get('nombre', 'Proyecto')}"
                    )
                    st.caption(estado.replace("_", " ").title())
                    confianza = proyecto.get("confianza", "por_revisar")
                    ultima_senal = proyecto.get("ultima_senal")
                    st.caption(
                        f"Evidencia: {confianza.replace('_', ' ').title()}"
                        + (f" · Última señal: {ultima_senal}" if ultima_senal else "")
                    )

                    st.markdown("**🔄 Ahora**")
                    st.write(
                        proyecto.get(
                            "ahora",
                            "Sin actividad registrada.",
                        )
                    )

                    fuentes_proyecto = proyecto.get("fuentes", [])
                    if fuentes_proyecto:
                        with st.expander("🔎 Señales rastreadas", expanded=False):
                            for fuente in fuentes_proyecto:
                                st.write(f"- {fuente.replace('_', ' ')}")

                    st.markdown("**➡️ Siguiente movimiento**")
                    st.write(
                        proyecto.get(
                            "siguiente",
                            "Pendiente de definir.",
                        )
                    )
    else:
        st.info(
            "Todavía no hay proyectos registrados en el mapa de avances. "
            "Agrega data/proyectos_actuales.json para activarlo."
        )

    st.markdown("---")

    trayectoria_profesional = cargar_json_publico(
        "data/trayectoria_profesional.json",
        {},
    )
    if trayectoria_profesional:
        st.subheader("💼 Trayectoria profesional contextual")
        st.write(trayectoria_profesional.get("summary", ""))
        st.caption(trayectoria_profesional.get("principle", ""))

        lineas_profesionales = trayectoria_profesional.get("lines", [])
        alta_confianza = sum(
            1 for linea in lineas_profesionales
            if linea.get("confidence") == "alta"
        )
        p1, p2, p3 = st.columns(3)
        p1.metric("Líneas rastreadas", len(lineas_profesionales))
        p2.metric("Evidencia alta", alta_confianza)
        p3.metric(
            "Pendientes de revisión",
            len(trayectoria_profesional.get("review_pending", [])),
        )

        for linea in lineas_profesionales:
            with st.expander(
                f"{linea.get('name', 'Línea profesional')} · "
                f"{linea.get('state', 'por revisar').replace('_', ' ')}",
                expanded=False,
            ):
                st.write(
                    "**Enfoques:** "
                    + ", ".join(linea.get("focus", []))
                )
                st.caption(
                    "Confianza: "
                    + linea.get("confidence", "por revisar").title()
                )
                st.write("**Evidencia contextual:**")
                for evidencia in linea.get("evidence", []):
                    st.write(f"- {evidencia.replace('_', ' ')}")

        matriz_experiencia = trayectoria_profesional.get("experience_matrix", [])
        if matriz_experiencia:
            with st.expander("🏛️ Trayectoria institucional reportada", expanded=True):
                st.caption(
                    "Periodos, cargos y proyectos sujetos a validación documental."
                )
                st.dataframe(
                    [
                        {
                            "Institución": registro.get("institution", ""),
                            "Periodo": registro.get("period", ""),
                            "Área": registro.get("area", ""),
                            "Proyectos o funciones": ", ".join(registro.get("projects", [])),
                            "Verificación": registro.get("evidence_status", "").replace("_", " "),
                        }
                        for registro in matriz_experiencia
                    ],
                    width="stretch",
                    hide_index=True,
                )

        resultados_reportados = trayectoria_profesional.get("reported_results", [])
        if resultados_reportados:
            with st.expander("📏 Habilidades con resultados reportados", expanded=True):
                st.warning(
                    "Las cifras son antecedentes por verificar; todavía no se presentan "
                    "como resultados certificados."
                )
                st.dataframe(
                    [
                        {
                            "Habilidad": resultado.get("skill", ""),
                            "Proyecto": resultado.get("project", ""),
                            "Resultado reportado": resultado.get("result", ""),
                            "Falta verificar": resultado.get("verification", "").replace("_", " "),
                        }
                        for resultado in resultados_reportados
                    ],
                    width="stretch",
                    hide_index=True,
                )

        with st.expander("🔄 Capacidades transferibles y revisión", expanded=False):
            st.markdown("**Capacidades transferibles**")
            for capacidad in trayectoria_profesional.get("transferable_capabilities", []):
                st.write(f"- {capacidad}")
            st.markdown("**Antes de publicar como perfil profesional**")
            for pendiente in trayectoria_profesional.get("review_pending", []):
                st.write(f"- {pendiente}")

        matriz_maestra = cargar_json_publico(
            trayectoria_profesional.get(
                "master_matrix",
                "data/matriz_trayectoria_evidencias_publico.json",
            ),
            {},
        )
        if matriz_maestra:
            st.subheader("🧾 Matriz maestra de trayectoria y evidencias")
            st.write(matriz_maestra.get("purpose", ""))
            st.caption(
                "Posicionamiento: " + matriz_maestra.get("positioning", "por revisar")
            )

            experiencias = matriz_maestra.get("experience", [])
            proyectos_estrella = matriz_maestra.get("star_projects", [])
            conflictos = matriz_maestra.get("open_conflicts", [])
            primarias = sum(
                1 for item in experiencias
                if item.get("level") == "primaria_verificada"
            )
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Registros", len(experiencias))
            m2.metric("Evidencia primaria", primarias)
            m3.metric("Proyectos estrella", len(proyectos_estrella))
            m4.metric("Conflictos abiertos", len(conflictos))

            st.dataframe(
                [
                    {
                        "Periodo": item.get("period", ""),
                        "Ámbito": item.get("scope", ""),
                        "Función": item.get("role", ""),
                        "Proyectos": item.get("projects", ""),
                        "Nivel": item.get("level", "").replace("_", " "),
                        "Revisión": item.get("status", "").replace("_", " "),
                    }
                    for item in experiencias
                ],
                width="stretch",
                hide_index=True,
            )

            with st.expander("⭐ Cuatro proyectos para el portafolio", expanded=True):
                for proyecto in proyectos_estrella:
                    st.markdown(f"**{proyecto.get('project', 'Proyecto')}**")
                    st.write(
                        f"Problema: {proyecto.get('problem', '')} · "
                        f"Arquitectura: {proyecto.get('architecture', '')}"
                    )
                    st.write(f"Resultado: {proyecto.get('result', '')}")
                    st.caption(
                        f"Evidencia: {proyecto.get('evidence', '')} · "
                        f"Estado: {proyecto.get('status', '').replace('_', ' ')}"
                    )

            with st.expander("⚖️ Contradicciones y decisiones de publicación", expanded=False):
                st.warning(
                    "Estos puntos permanecen abiertos: la aplicación no elige "
                    "automáticamente la versión más favorable."
                )
                for conflicto in conflictos:
                    st.markdown(f"**{conflicto.get('topic', 'Por revisar')}**")
                    st.write("Versiones: " + " · ".join(conflicto.get("versions", [])))
                    st.caption("Decisión: " + conflicto.get("decision", ""))

        carta_compromisos = cargar_json_publico(
            "data/carta_compromisos_2026_2027.json",
            {},
        )
        if carta_compromisos:
            st.subheader("🧭 Compromisos 2026–2027")
            st.info(carta_compromisos.get("central_direction", ""))
            st.write(carta_compromisos.get("declaration", ""))
            st.caption(
                "Estado: "
                + carta_compromisos.get("status", "por revisar").replace("_", " ")
                + " · Este marco orienta trabajo futuro; no es evidencia histórica."
            )

            compromisos_prioritarios = carta_compromisos.get(
                "priority_commitments", []
            )
            for compromiso in compromisos_prioritarios:
                with st.expander(
                    f"{compromiso.get('priority', '–')}. "
                    f"{compromiso.get('name', 'Compromiso')}",
                    expanded=compromiso.get("priority") == 1,
                ):
                    st.write(compromiso.get("rule", ""))
                    st.markdown(
                        "**Evidencia de cumplimiento:** "
                        + compromiso.get("completion_evidence", "")
                    )
                    st.caption(
                        "Estado: "
                        + compromiso.get("state", "por revisar").replace("_", " ")
                    )

            compromisos_medibles = carta_compromisos.get(
                "measurable_commitments", []
            )
            with st.expander("📋 Tablero de compromisos medibles", expanded=True):
                st.dataframe(
                    [
                        {
                            "Compromiso": item.get("commitment", ""),
                            "Evidencia de cumplimiento": item.get("evidence", ""),
                            "Estado": item.get("current_state", "").replace("_", " "),
                            "Siguiente acción": item.get("next_action", ""),
                        }
                        for item in compromisos_medibles
                    ],
                    width="stretch",
                    hide_index=True,
                )

            with st.expander("🚦 Etapas y criterio para avanzar", expanded=False):
                st.dataframe(
                    [
                        {
                            "Etapa": etapa.get("stage", "").replace("_", " ").title(),
                            "Criterio de salida": etapa.get("exit_criterion", ""),
                        }
                        for etapa in carta_compromisos.get("project_maturity", [])
                    ],
                    width="stretch",
                    hide_index=True,
                )
                politica = carta_compromisos.get("focus_policy", {})
                st.warning(
                    "Máximo de prioridades simultáneas: "
                    + str(politica.get("maximum_simultaneous_priorities", 3))
                    + ". "
                    + politica.get("new_project_rule", "")
                )
                st.success(carta_compromisos.get("supreme_commitment", ""))

            ejecucion_compromiso = carta_compromisos.get(
                "commitment_2_execution", {}
            )
            if ejecucion_compromiso:
                st.subheader("🛠️ Compromiso 2 activo · Producto terminado")
                st.write(ejecucion_compromiso.get("objective", ""))
                st.dataframe(
                    [
                        {
                            "Orden": item.get("order", ""),
                            "Proyecto": item.get("project", ""),
                            "Etapa actual": item.get("current_stage", "").replace("_", " "),
                            "Siguiente puerta": item.get("next_gate", ""),
                        }
                        for item in ejecucion_compromiso.get("ordered_backlog", [])
                    ],
                    width="stretch",
                    hide_index=True,
                )
                with st.expander("Definición común de terminado", expanded=False):
                    for criterio in ejecucion_compromiso.get("definition_of_done", []):
                        st.write(f"- {criterio}")
                    st.warning(ejecucion_compromiso.get("rule", ""))

        st.markdown("---")

    radar_profesional = cargar_json_publico(
        "data/radar_red_profesional_publico.json",
        {},
    )
    if radar_profesional:
        st.subheader("📡 Red profesional y radar de oportunidades")
        st.write(radar_profesional.get("purpose", ""))
        st.caption(
            "Vista pública agregada: nombres, mensajes, rutas locales y evidencia "
            "visual permanecen privados."
        )

        resumen_radar = radar_profesional.get("summary", {})
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Registros de ruta", resumen_radar.get("route_records", 0))
        r2.metric("Fuentes configuradas", resumen_radar.get("configured_public_sources", 0))
        r3.metric("Nodos de oportunidad", resumen_radar.get("opportunity_nodes", 0))
        r4.metric("Duplicados detectados", resumen_radar.get("duplicate_files_detected", 0))

        with st.expander("🧭 Línea de avance", expanded=True):
            for numero, paso in enumerate(radar_profesional.get("progress_line", []), 1):
                st.write(f"{numero}. {paso}")

        col_red, col_fuentes = st.columns(2)
        with col_red:
            st.markdown("**Capas de la red**")
            for capa in radar_profesional.get("network_layers", []):
                st.write(f"- {capa}")
        with col_fuentes:
            st.markdown("**Familias rastreadas**")
            for grupo in radar_profesional.get("source_groups", []):
                st.write(
                    f"- {grupo.get('name', 'Fuente')} · "
                    f"{grupo.get('files', 0)} archivo(s) · "
                    f"{grupo.get('status', 'por_revisar').replace('_', ' ')}"
                )

        with st.expander("⚠️ Limitaciones técnicas actuales", expanded=False):
            for limitacion in radar_profesional.get("limitations", []):
                st.write(f"- {limitacion}")

        señales_profesionales = radar_profesional.get("anonymized_signals", [])
        if señales_profesionales:
            with st.expander("🤝 Señales profesionales anonimizadas", expanded=True):
                st.caption(
                    "Se conservan únicamente contexto, estado y próxima acción; "
                    "no se muestran nombres ni mensajes."
                )
                st.dataframe(
                    [
                        {
                            "Fecha": señal.get("date", ""),
                            "Canal": señal.get("channel", "").replace("_", " "),
                            "Contexto": señal.get("institutional_context", ""),
                            "Estado": señal.get("status", "").replace("_", " "),
                            "Próxima acción": señal.get("next_action", ""),
                        }
                        for señal in señales_profesionales
                    ],
                    width="stretch",
                    hide_index=True,
                )

        reglas_eticas = radar_profesional.get("ethical_guardrails", [])
        if reglas_eticas:
            with st.expander("🛡️ Límites éticos y de privacidad", expanded=False):
                for regla in reglas_eticas:
                    st.write(f"- {regla}")

        st.markdown("---")

    gemelo_digital = cargar_json_publico(
        "data/gemelo_digital_publico.json",
        {},
    )
    if gemelo_digital:
        st.subheader("🌐 Gemelo Digital Municipal")
        st.write(gemelo_digital.get("definition", ""))
        st.caption(
            "Estado actual: "
            + gemelo_digital.get("status", "por_revisar").replace("_", " ")
        )

        hallazgo_gemelo = gemelo_digital.get("discovery", {})
        base_gemelo = gemelo_digital.get("reported_baseline", {})
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("Artefactos principales", len(gemelo_digital.get("primary_artifacts", [])))
        g2.metric("Menciones locales", hallazgo_gemelo.get("unique_local_mentions", 0))
        g3.metric("Localidades reportadas", base_gemelo.get("localities", 0))
        g4.metric("Población reportada", base_gemelo.get("population", 0))
        st.caption(base_gemelo.get("status", "").replace("_", " "))

        col_madurez, col_ruta = st.columns(2)
        with col_madurez:
            st.markdown("**Madurez verificada**")
            for capa in gemelo_digital.get("maturity", []):
                st.write(
                    f"- {capa.get('layer', 'Capa')}: "
                    f"{capa.get('status', 'por revisar').replace('_', ' ')}"
                )
        with col_ruta:
            st.markdown("**Ruta mínima viable**")
            for numero, paso in enumerate(gemelo_digital.get("minimum_viable_path", []), 1):
                st.write(f"{numero}. {paso}")

        with st.expander("🛡️ Privacidad y referencias técnicas", expanded=False):
            for regla in gemelo_digital.get("guardrails", []):
                st.write(f"- {regla}")
            for referencia in gemelo_digital.get("external_references", []):
                st.markdown(
                    f"- [{referencia.get('name', 'Referencia')}]"
                    f"({referencia.get('url', '')}) — {referencia.get('use', '')}"
                )

        with st.expander("🧵 Evolución y evidencia localizada", expanded=True):
            for etapa in gemelo_digital.get("evolution_timeline", []):
                st.markdown(
                    f"**{etapa.get('period', 'Periodo por confirmar')} · "
                    f"{etapa.get('milestone', 'Hito')}**"
                )
                st.write(etapa.get("evidence", ""))
                st.caption(
                    "Verificación: "
                    + etapa.get("verification", "por_revisar").replace("_", " ")
                )

        afirmaciones_excluidas = gemelo_digital.get("excluded_unverified_claims", [])
        if afirmaciones_excluidas:
            with st.expander("🚫 Afirmaciones todavía no demostradas", expanded=False):
                for afirmacion in afirmaciones_excluidas:
                    st.write(f"- {afirmacion}")

        st.markdown("---")

    # ============================================
    # CONTEXTO INICIAL
    # ============================================
    st.subheader("📋 Contexto Inicial")

    with st.expander("🧠 Gestión del contexto y las ideas", expanded=False):
        modo_contexto = st.radio(
            "¿Cómo quieres trabajar en este momento?",
            [
                "Incubación libre",
                "Consolidar lo que ya surgió",
            ],
            horizontal=True,
            key="modo_contexto",
        )

        acciones_contexto = []
        notas_contexto = ""
        if modo_contexto == "Incubación libre":
            st.info(
                "Conversa y explora sin definir una conclusión prematura. "
                "Cuando aparezca una idea importante, puedes anotarla aquí sin interrumpir el hilo."
            )
            notas_contexto = st.text_area(
                "Idea emergente o conexión que no quieres perder (opcional)",
                key="nota_incubacion",
            )
        else:
            st.info(
                "Revisa lo acumulado y decide qué debe convertirse en checkpoint, "
                "hilo derivado, tarea o idea pendiente."
            )
            acciones_contexto = st.multiselect(
                "¿Qué necesitas organizar?",
                [
                    "Crear checkpoint",
                    "Separar hilos",
                    "Registrar decisiones",
                    "Guardar ideas pendientes",
                    "Relacionar conversaciones",
                    "Reducir el contexto activo",
                    "Todavía no estoy seguro",
                ],
                key="acciones_contexto",
                placeholder="Puedes elegir varias acciones",
            )
            notas_contexto = st.text_area(
                "Notas para la consolidación (opcional)",
                key="nota_consolidacion",
            )

        st.caption(
            "CO•RA conserva el texto completo como fuente y trabaja con síntesis, checkpoints "
            "y fragmentos relevantes. El conteo automático de tokens y la memoria persistente "
            "todavía no están habilitados en el modo público."
        )

    claridad_objetivo = st.radio(
        "¿Qué tan claro tienes lo que quieres hacer?",
        [
            "Tengo claro mi objetivo",
            "Tengo una idea, pero no sé cómo formularla",
            "Todavía no estoy seguro; quiero explorar",
        ],
        horizontal=True,
    )

    objetivo = ""
    exploracion = []
    if claridad_objetivo == "Tengo claro mi objetivo":
        objetivo = st.text_input("¿Qué quieres lograr?")
    else:
        st.caption(
            "No necesitas definir una meta todavía. Selecciona una o varias "
            "opciones y CO•RA te ayudará a encontrar posibles rutas."
        )
        exploracion = st.multiselect(
            "¿Qué describe mejor lo que está pasando?",
            [
                "Observé algo interesante",
                "Tengo un problema, pero no conozco la causa",
                "Quiero relacionar varias cosas",
                "Quiero recuperar algo que trabajé antes",
                "Quiero evitar repetir trabajo",
                "Solo quiero explorar",
                "No estoy seguro",
            ],
            placeholder="Puedes elegir varias opciones",
        )
        idea_inicial = st.text_area(
            "Cuéntame lo que tienes en mente (opcional)",
            placeholder="Puede ser una observación, una duda o algo que te llamó la atención.",
        )
        partes_objetivo = exploracion + ([idea_inicial.strip()] if idea_inicial.strip() else [])
        objetivo = " | ".join(partes_objetivo)

    col1, col2 = st.columns(2)

    with col1:
        recursos = st.text_area("¿Con qué cuentas ahora?")

    with col2:
        observacion = st.text_area("¿Qué estás observando?")
        nombre = st.text_input("¿Cómo quieres que te llame?", value=usuario)
    
    st.markdown("---")
    st.subheader("🧭 Mapa Abierto de Conocimiento")
    st.caption(
        "Las áreas frecuentes son puntos de entrada, no límites. Puedes comenzar "
        "con una disciplina, problema, idea, hipótesis, tesis, teoría, ley o relación todavía sin clasificar."
    )

    tema_abierto = st.text_input(
        "¿Qué quieres explorar?",
        placeholder="Escribe una palabra, observación, pregunta o conexión posible",
        key="tema_mapa_abierto",
    )
    tipos_abiertos = st.multiselect(
        "¿Cómo describirías lo que tienes? (opcional)",
        [
            "Disciplina o área",
            "Tema",
            "Problema",
            "Idea emergente",
            "Hipótesis",
            "Tesis",
            "Teoría",
            "Ley o principio",
            "Método o modelo",
            "Relación entre varias cosas",
            "Todavía no lo sé",
        ],
        key="tipos_mapa_abierto",
        placeholder="Puedes elegir varias opciones",
    )
    if st.button("🧭 Explorar sin limitar el área", use_container_width=True):
        st.session_state.area_seleccionada = 'mapa_abierto'
        st.session_state.tema_abierto_activo = tema_abierto.strip()
        st.session_state.tipos_abiertos_activos = tipos_abiertos

    st.markdown("---")
    st.subheader("🎯 Áreas frecuentes de tu trayectoria")

    # Mostrar accesos frecuentes como botones; el mapa abierto tiene su propia entrada.
    cols = st.columns(4)
    areas_lista = [
        item for item in AREAS_CONOCIMIENTO.items()
        if item[0] != 'mapa_abierto'
    ]
    
    for idx, (area_id, area_data) in enumerate(areas_lista):
        col = cols[idx % 4]
        with col:
            if st.button(
                f"{area_data['icono']} {area_data['nombre']}",
                key=f"area_{area_id}",
                use_container_width=True
            ):
                st.session_state.area_seleccionada = area_id
    
    # Cuando se selecciona un área
    if 'area_seleccionada' in st.session_state:
        area_id = st.session_state.area_seleccionada
        area = dict(AREAS_CONOCIMIENTO[area_id])

        if area_id == 'mapa_abierto':
            tema_activo = st.session_state.get('tema_abierto_activo', '')
            tipos_activos = st.session_state.get('tipos_abiertos_activos', [])
            if tema_activo:
                area['nombre'] = tema_activo
                area['descripcion'] = "Exploración abierta: " + (
                    ", ".join(tipos_activos) if tipos_activos else "sin clasificación obligatoria"
                )
                area['pregunta'] = f"¿Qué quieres comprender, comprobar o relacionar sobre {tema_activo}?"
                area['palabras_clave'] = [
                    palabra.lower() for palabra in tema_activo.split() if len(palabra) > 2
                ]
        
        # Cargar historial y rastrear contextos
        historial = cargar_conversaciones()
        contextos = rastrear_contextos_previos(area_id, historial)
        
        st.markdown("---")
        st.subheader(f"{area['icono']} {area['nombre']}")
        st.caption(area['descripcion'])
        
        # Mostrar recomendación
        recomendacion = generar_recomendacion(area['nombre'], contextos)
        st.info(f"**{recomendacion}**")
        
        # Mostrar contextos previos detectados
        if contextos:
            with st.expander(f"🔍 {len(contextos)} contextos previos detectados"):
                for ctx in contextos:
                    pinned = "📌" if ctx['is_pinned'] else "💬"
                    st.write(f"{pinned} {ctx['titulo']} (relevancia: {ctx['relevancia']:.2f})")
        
        # Mostrar áreas conectadas
        areas_conectadas = area.get('conectadas', [])
        if areas_conectadas:
            st.markdown("**🔗 Áreas conectadas con tu trayectoria:**")
            cols_conn = st.columns(min(3, len(areas_conectadas)))
            for idx, area_conn_id in enumerate(areas_conectadas):
                with cols_conn[idx % 3]:
                    area_conn = AREAS_CONOCIMIENTO.get(area_conn_id, {})
                    contextos_conn = rastrear_contextos_previos(area_conn_id, historial)
                    fortaleza = "✅" if len(contextos_conn) >= 3 else ""
                    st.markdown(
                        f"**{area_conn.get('icono', '')} {area_conn.get('nombre', area_conn_id)}**\n\n"
                        f"{fortaleza} {len(contextos_conn)} contextos"
                    )
        
        # Pregunta adaptada
        pregunta = area['pregunta']
        st.markdown(f"### 📝 Pregunta · {pregunta}")
        
        # Formulario de respuesta
        st.markdown("#### 1. Punto A · ¿Qué piensas al respecto?")
        st.caption("Antes de buscar una respuesta correcta, cuéntame cómo lo entiendes tú.")
        modelo_mental = st.text_area("Tu comprensión actual", height=100, key=f"modelo_{area_id}")
        
        st.markdown("#### 2. ¿Qué puedes explicar con lo que sabes ahora?")
        st.caption("Intenta responder la pregunta")
        respuesta_ejecucion = st.text_area("Tu respuesta", height=100, key=f"respuesta_{area_id}")
        
        # Botón de análisis
        if st.button("🔍 Analizar y Anclar", type="primary", key=f"analizar_{area_id}"):
            if modelo_mental and respuesta_ejecucion:
                with st.spinner("Procesando a través del núcleo CO•RA..."):
                    if token and ENABLE_GITHUB_WRITES:
                        respuesta_github = bridge.anclar_evento(
                            usuario=nombre,
                            evento_id="TUTOR_MENTAL_MODEL_SUBMITTED",
                            payload={
                                "area": area_id,
                                "area_nombre": area['nombre'],
                                "pregunta": pregunta,
                                "modelo_mental": modelo_mental,
                                "respuesta_ejecucion": respuesta_ejecucion,
                                "objetivo": objetivo,
                                "recursos": recursos,
                                "observacion": observacion,
                                "modo_contexto": modo_contexto,
                                "acciones_contexto": acciones_contexto,
                                "notas_contexto": notas_contexto,
                                "contextos_previos": len(contextos)
                            }
                        )
                        if respuesta_github and respuesta_github.ok:
                            st.success("✅ Evento anclado en Matriz Dorsal")
                        else:
                            st.error("No fue posible guardar el evento en GitHub.")
                    else:
                        evento_local = {
                            "area": area_id,
                            "pregunta": pregunta,
                            "modelo_mental": modelo_mental,
                            "respuesta_ejecucion": respuesta_ejecucion,
                            "modo_contexto": modo_contexto,
                            "acciones_contexto": acciones_contexto,
                            "notas_contexto": notas_contexto
                        }
                        st.download_button(
                            "⬇️ Descargar evento para revisión local",
                            data=json.dumps(evento_local, indent=2, ensure_ascii=False),
                            file_name="evento_cora.json",
                            mime="application/json"
                        )
                    
                    st.info("🔄 Analizando trayectoria de aprendizaje...")
            else:
                st.warning("⚠️ Por favor completa ambos campos para continuar")

# ============================================
# TAB 2: CONVERSACIONES Y REGISTROS
# ============================================
with tab2:
    st.subheader("📚 Conversaciones y registros rastreados")
    st.caption(
        "Títulos y metadatos procedentes de ChatGPT, Qwen, Gemini, "
        "Copilot, Kimi, Runable y otras fuentes autorizadas."
    )
    
    conversaciones = cargar_conversaciones()
    
    if conversaciones:
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Registros indexados", len(conversaciones))
        with col2:
            ancladas = sum(1 for c in conversaciones if c.get('is_pinned'))
            st.metric("Conversaciones Ancladas", ancladas)
        with col3:
            categorias_unicas = len(set(c.get('categoria', 'sin_clasificar') for c in conversaciones))
            st.metric("Categorías Exploradas", categorias_unicas)
        
        st.markdown("---")
        
        # Filtros
        col_filtro1, col_filtro2 = st.columns(2)
        with col_filtro1:
            categorias = list(set(c.get('categoria', 'sin_clasificar') for c in conversaciones))
            filtro_categoria = st.multiselect(
                "Filtrar por categoría",
                categorias,
                default=[]
            )
        with col_filtro2:
            solo_ancladas = st.checkbox("Mostrar solo ancladas 📌")
        
        # Aplicar filtros
        conversaciones_filtradas = conversaciones
        if filtro_categoria:
            conversaciones_filtradas = [c for c in conversaciones_filtradas if c.get('categoria') in filtro_categoria]
        if solo_ancladas:
            conversaciones_filtradas = [c for c in conversaciones_filtradas if c.get('is_pinned')]
        
        st.markdown(f"**{len(conversaciones_filtradas)} registros encontrados**")
        
        # Mostrar conversaciones
        for conv in conversaciones_filtradas[:30]:
            pinned = "📌" if conv.get('is_pinned') else "💬"
            categoria = conv.get('categoria', 'sin_clasificar')
            
            with st.expander(f"{pinned} {conv.get('titulo', 'Sin título')} [{categoria}]"):
                st.write(f"**Categoría:** {categoria}")
                st.write(f"**Anclada:** {'Sí' if conv.get('is_pinned') else 'No'}")
                st.write(f"**Fecha extracción:** {conv.get('fecha_extraccion', 'N/A')}")
                if conv.get('url_completa'):
                    st.link_button("Ver conversación", conv['url_completa'])
    else:
        st.info("No hay conversaciones públicas disponibles. El historial privado permanece fuera del repositorio.")

# ============================================
# TAB 3: MEMORY BANK
# ============================================
with tab3:
    st.subheader("🧠 Memory Bank")
    st.caption("Conexión con GitHub para persistencia de datos")
    
    if token:
        if st.button("🔄 Cargar contexto desde GitHub"):
            with st.spinner("Cargando..."):
                contexto = bridge.leer_contexto(
                    f"memory_bank/usuarios/{nombre}/contexto_unificado.json"
                )
                if contexto:
                    st.success("✅ Contexto cargado")
                    st.json(contexto)
                else:
                    st.info("No hay contexto previo. Este es tu Punto A inicial.")
        
        st.markdown("---")
        st.subheader("📊 Eventos en Matriz Dorsal")
        
        if st.button("Ver eventos recientes"):
            eventos = bridge.leer_contexto(
                f"matriz_dorsal/usuarios/{nombre}/eventos.jsonl"
            )
            if eventos:
                st.write(f"**Total de eventos:** {len(eventos) if isinstance(eventos, list) else 'N/A'}")
            else:
                st.info("No hay eventos registrados aún.")
    else:
        st.info("Memory Bank privado no configurado. Los visitantes no necesitan proporcionar tokens.")

# ============================================
# TAB 4: AGENTES + CONVERSACIONES
# ============================================
with tab4:
    sub_catalogo, sub_conversaciones = st.tabs([
        "🧩 Catálogo",
        "💬 Conversaciones",
    ])

    # --------------------------------------------
    # CATÁLOGO PÚBLICO
    # --------------------------------------------
    with sub_catalogo:
        st.subheader("🤝 Catálogo público de agentes")
        st.caption(
            "Capacidades observadas y pendientes de validación; "
            "no ejecuta ni envía tareas."
        )

        inventario_agentes = cargar_json_publico(
            "data/inventario_agentes_publico.json",
            {},
        )
        if inventario_agentes:
            resumen_agentes = inventario_agentes.get("summary", {})
            st.markdown("### 🗺️ Panorama e inventario de agentes")
            i1, i2, i3 = st.columns(3)
            i1.metric("Agentes indexados", resumen_agentes.get("agents_indexed_locally", 0))
            i2.metric("Categorías", resumen_agentes.get("categories", 0))
            i3.metric("Con metadatos de acceso", resumen_agentes.get("with_access_metadata", 0))
            st.link_button(
                "Abrir paisaje público de referencia",
                inventario_agentes.get("source_reference"),
            )

            with st.expander("📈 Línea de avance del inventario", expanded=True):
                estados_avance = {
                    "completado": "✅",
                    "en_progreso": "🟡",
                    "pendiente": "⚪",
                }
                for paso in inventario_agentes.get("progress_line", []):
                    icono_paso = estados_avance.get(paso.get("status"), "⚪")
                    st.write(
                        f"{icono_paso} **{paso.get('step')}. {paso.get('name')}** — "
                        f"{paso.get('result')}"
                    )

            with st.expander("📊 Cobertura por categoría y acceso", expanded=False):
                st.markdown("**Categorías principales**")
                st.dataframe(
                    inventario_agentes.get("top_categories", []),
                    use_container_width=True,
                    hide_index=True,
                )
                col_access, col_pricing = st.columns(2)
                with col_access:
                    st.markdown("**Acceso**")
                    st.dataframe(inventario_agentes.get("access", []), hide_index=True)
                with col_pricing:
                    st.markdown("**Precio**")
                    st.dataframe(inventario_agentes.get("pricing", []), hide_index=True)

            st.warning(
                "Las fichas completas permanecen locales hasta revisar fuente, "
                "vigencia, licencia, duplicados y pertinencia para cada proyecto."
            )
            st.markdown("---")

        catalogo = cargar_json_publico(
            "data/catalogo_agentes_publico.json",
            {"agents": []}
        )

        fuentes_evaluacion = catalogo.get("evaluation_sources", [])
        if fuentes_evaluacion:
            st.markdown("### 📊 Fuentes públicas de descubrimiento y evaluación")
            for fuente in fuentes_evaluacion:
                col_fuente, col_enlace = st.columns([3, 1])
                with col_fuente:
                    st.write(f"**{fuente.get('display_name', 'Fuente externa')}**")
                    tipo_fuente = fuente.get("source_type", "referencia_externa")
                    st.caption(
                        "Tipo: " + tipo_fuente.replace("_", " ")
                    )
                    st.caption(fuente.get("usage_note", "Referencia comparativa."))
                    senales = fuente.get("signals", [])
                    if senales:
                        st.caption(
                            "Señales: "
                            + ", ".join(s.replace("_", " ") for s in senales)
                        )
                with col_enlace:
                    if fuente.get("url"):
                        st.link_button(
                            "Abrir fuente viva",
                            fuente["url"],
                            use_container_width=True,
                        )
            st.caption(
                "Los rankings externos cambian con el tiempo y se usan como "
                "evidencia complementaria, no como decisión automática."
            )
            st.markdown("---")

        for agente in catalogo.get("agents", []):
            with st.expander(
                f"{agente.get('display_name', agente.get('agent_id'))} · "
                f"{agente.get('status', 'sin estado')}"
            ):
                st.write(
                    f"**Acceso:** {agente.get('access_method', 'por definir')}"
                )
                st.write("**Capacidades:**")
                for capacidad in agente.get("capabilities", []):
                    st.write(f"- {capacidad}")

        st.info(
            "El despacho automático está desactivado y todo envío externo "
            "requiere aprobación humana."
        )

    # --------------------------------------------
    # CONVERSACIONES
    # --------------------------------------------
with sub_conversaciones:
    st.subheader("🔎 Rastreo de conversaciones")
    st.caption(
        "CO•RA identifica, deduplica e indexa conversaciones existentes. "
        "No crea conversaciones ni publica su contenido."
    )

    inventario_local = cargar_json_publico(
        "data/fuentes_locales_publico.json",
        {},
    )
    if inventario_local:
        resumen_local = inventario_local.get("summary", {})
        with st.expander("🖥️ Fuentes locales detectadas", expanded=False):
            st.warning(
                "Este es un inventario sanitizado. Streamlit Cloud no puede "
                "leer directamente las carpetas del equipo ni sincronizarlas "
                "sin un puente local autorizado."
            )
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Archivos observados", resumen_local.get("files_observed", 0))
            c2.metric("Candidatos", resumen_local.get("candidate_files", 0))
            c3.metric("Fuentes", len(inventario_local.get("sources", [])))
            c4.metric(
                "Grupos duplicados",
                resumen_local.get("exact_duplicate_groups", 0),
            )

            filas_fuentes = [
                {
                    "Fuente": fuente.get("name"),
                    "Candidatos": fuente.get("candidates"),
                    "Tamaño MB": fuente.get("size_mb"),
                    "Encaminar a": fuente.get("route", "por_clasificar").replace("_", " "),
                    "Estado": fuente.get("status", "pendiente").replace("_", " "),
                }
                for fuente in inventario_local.get("sources", [])
            ]
            if filas_fuentes:
                st.dataframe(
                    filas_fuentes,
                    use_container_width=True,
                    hide_index=True,
                )

            correcciones = inventario_local.get("routing_corrections", [])
            if correcciones:
                st.markdown("#### Encaminamientos corregidos")
                for correccion in correcciones:
                    st.write(
                        f"- **{correccion.get('artifact')}** → "
                        f"{correccion.get('route', '').replace('_', ' ')} "
                        f"({correccion.get('reason', 'sin detalle')})"
                    )

            descubrimiento = inventario_local.get("latest_discovery", {})
            if descubrimiento:
                st.markdown("#### 🆕 Descubrimiento local reciente")
                st.caption(descubrimiento.get("policy", ""))
                fuentes_recientes = descubrimiento.get("sources", [])
                d1, d2, d3 = st.columns(3)
                d1.metric("Nuevas fuentes", descubrimiento.get("sources_reviewed", 0))
                d2.metric(
                    "Registros índice administrativo",
                    next(
                        (
                            fuente.get("records_observed", 0)
                            for fuente in fuentes_recientes
                            if fuente.get("alias") == "indice_administrativo_por_tipo"
                        ),
                        0,
                    ),
                )
                d3.metric(
                    "Registros índice general",
                    next(
                        (
                            fuente.get("records_observed", 0)
                            for fuente in fuentes_recientes
                            if fuente.get("alias") == "indice_general_por_tipo"
                        ),
                        0,
                    ),
                )
                st.dataframe(
                    [
                        {
                            "Fuente contextual": fuente.get("alias", "").replace("_", " "),
                            "Tipo": fuente.get("kind", "").replace("_", " "),
                            "Archivos": fuente.get("files", 0),
                            "Registros": fuente.get("records_observed"),
                            "Encaminar a": fuente.get("route", "").replace("_", " "),
                            "Estado": fuente.get("status", "").replace("_", " "),
                        }
                        for fuente in fuentes_recientes
                    ],
                    width="stretch",
                    hide_index=True,
                )
                with st.expander("Hallazgos y siguientes acciones", expanded=False):
                    st.markdown("**Hallazgos**")
                    for hallazgo in descubrimiento.get("findings", []):
                        st.write(f"- {hallazgo}")
                    st.markdown("**Siguientes acciones**")
                    for accion in descubrimiento.get("next_actions", []):
                        st.write(f"- {accion}")

            indice_contextual = cargar_json_publico(
                "data/indice_contextual_relativo.json",
                {},
            )
            if indice_contextual:
                st.markdown("#### 🧭 Índice relativo sólo contextual")
                st.caption(
                    "Agrupa señales por contexto sin conservar rutas, nombres "
                    "de archivos, accesos directos ni contenido. Las categorías "
                    "pueden superponerse."
                )
                contextos_relativos = [
                    {
                        "Contexto": item.get("context", "sin_contexto").replace("_", " "),
                        "Coincidencias": item.get("matches", 0),
                        "Encaminar a": item.get("route", "revision").replace("_", " "),
                        "Prioridad": item.get("priority", "low"),
                    }
                    for item in indice_contextual.get("contexts", [])
                ]
                st.dataframe(
                    contextos_relativos,
                    use_container_width=True,
                    hide_index=True,
                )

    with st.expander("📤 Registrar o rastrear fuentes", expanded=False):
        archivos_conversacion = st.file_uploader(
            "Sube exportaciones o archivos con conversaciones",
            type=["json", "jsonl", "txt", "md", "zip"],
            accept_multiple_files=True,
            key="upload_conversaciones_agentes",
        )
        st.caption(
            "El contenido se procesa sólo durante esta sesión; "
            "el índice exportado contiene metadatos y localizadores."
        )

        if archivos_conversacion and st.button(
            "🔎 Rastrear conversaciones",
            type="primary",
            key="procesar_conversaciones_agentes",
        ):
            detectadas = []
            for archivo in archivos_conversacion:
                detectadas.extend(procesar_archivo_conversaciones(archivo))

            anteriores = st.session_state.get(
                "conversaciones_importadas", []
            )
            fusion = fusionar_conversaciones_session(
                {},
                anteriores + detectadas,
                str(INDICE_CONVERSACIONES),
            )
            canonicas = cargar_indice_como_conversaciones(
                str(INDICE_CONVERSACIONES)
            )
            st.session_state.conversaciones_importadas = [
                conv for cid, conv in fusion.items() if cid not in canonicas
            ]
            st.session_state.resultado_rastreo = {
                "detectadas": len(detectadas),
                "nuevas": max(0, len(fusion) - len(canonicas)),
            }
            st.rerun()

    resultado = st.session_state.get("resultado_rastreo")
    if resultado:
        st.success(
            f"✅ {resultado['detectadas']} detectadas; "
            f"{resultado['nuevas']} entradas nuevas tras deduplicar."
        )

    # El índice canónico siempre alimenta la lista. Las detecciones de la
    # sesión se superponen sólo en memoria hasta que el usuario las exporta.
    conversaciones_agentes = fusionar_conversaciones_session(
        cargar_indice_como_conversaciones(str(INDICE_CONVERSACIONES)),
        st.session_state.get("conversaciones_importadas", []),
        str(INDICE_CONVERSACIONES),
    )
    if "active_conversation_id" not in st.session_state:
        st.session_state.active_conversation_id = None

    indice_exportable = exportar_indice(conversaciones_agentes)
    st.download_button(
        "⬇️ Exportar índice de metadatos",
        data=json.dumps(indice_exportable, indent=2, ensure_ascii=False),
        file_name="conversaciones_indice.json",
        mime="application/json",
        use_container_width=False,
    )
    with st.expander("📥 Integrar un historial grande (+1,500 títulos)", expanded=False):
        st.markdown(
            "1. Solicita la exportación de datos de ChatGPT.\n"
            "2. Localiza `conversations.json` dentro del ZIP.\n"
            "3. Súbelo en **Registrar o rastrear fuentes**.\n"
            "4. CO•RA extraerá títulos y metadatos, deduplicará y permitirá "
            "exportar el índice.\n"
            "5. Revisa los títulos sensibles antes de publicar el archivo resultante."
        )
        st.warning(
            "El historial del navegador no equivale al historial completo de "
            "conversaciones. Para recuperar más de 1,500 títulos se necesita "
            "la exportación `conversations.json`."
        )

    st.markdown("---")
    col_lista, col_detalle = st.columns([1, 2], gap="large")

    with col_lista:
        st.markdown("### 📚 Conversaciones detectadas")
        st.caption(
            f"{len(conversaciones_agentes)} títulos disponibles en el índice."
        )
        filtro = st.text_input(
            "🔎 Buscar",
            placeholder="Título, agente, fuente o proyecto...",
            key="buscar_conversacion_agente",
        ).strip().lower()

        lista = sorted(
            conversaciones_agentes.values(),
            key=lambda c: c.get("updated_at") or c.get("fecha") or "",
            reverse=True,
        )

        fuentes_lista = sorted({
            str(conv.get("fuente") or "sin_fuente")
            for conv in lista
        })
        filtro_fuente = st.selectbox(
            "Fuente",
            ["Todas"] + fuentes_lista,
            key="filtro_fuente_conversaciones",
        )
        if filtro_fuente != "Todas":
            lista = [
                conv for conv in lista
                if str(conv.get("fuente") or "sin_fuente") == filtro_fuente
            ]
        if filtro:
            lista = [
                conv for conv in lista
                if filtro in " ".join([
                    str(conv.get("titulo") or ""),
                    str(conv.get("fuente") or ""),
                    str(conv.get("agente") or ""),
                    str(conv.get("proyecto") or ""),
                ]).lower()
            ]

        if not lista:
            st.info("No hay conversaciones indexadas con este filtro.")

        tamano_pagina = st.selectbox(
            "Títulos por página",
            [25, 50, 100],
            index=0,
            key="tamano_pagina_conversaciones",
        )
        total_paginas = max(1, (len(lista) + tamano_pagina - 1) // tamano_pagina)
        pagina = st.number_input(
            "Página",
            min_value=1,
            max_value=total_paginas,
            value=1,
            step=1,
            key="pagina_conversaciones",
        )
        inicio_pagina = (pagina - 1) * tamano_pagina
        lista_pagina = lista[inicio_pagina:inicio_pagina + tamano_pagina]
        st.caption(
            f"Página {pagina} de {total_paginas} · "
            f"{len(lista)} títulos coincidentes"
        )

        for conv in lista_pagina:
            cid = conv.get("conversation_id") or conv.get("id")
            activo = cid == st.session_state.active_conversation_id
            prefijo = "🟢" if activo else "💬"
            if st.button(
                f"{prefijo} {conv.get('titulo', 'Sin título')}",
                key=f"abrir_{cid}",
                use_container_width=True,
            ):
                st.session_state.active_conversation_id = cid
                st.rerun()
            st.caption(
                " · ".join(filter(None, [
                    conv.get("agente"),
                    conv.get("fuente"),
                    conv.get("proyecto"),
                ]))
            )

    with col_detalle:
        active_id = st.session_state.active_conversation_id
        conversacion = conversaciones_agentes.get(active_id)
        if not conversacion:
            st.info("Selecciona una conversación para revisar sus metadatos.")
        else:
            st.markdown(
                f"### 💬 {conversacion.get('titulo', 'Sin título')}"
            )
            metadatos = {
                "fuente": conversacion.get("fuente"),
                "agente": conversacion.get("agente"),
                "fecha": conversacion.get("fecha"),
                "proyecto": conversacion.get("proyecto"),
                "hash": conversacion.get("hash"),
                "locator": conversacion.get("locator") or {},
                "estado": (
                    conversacion.get("tracking_status")
                    or conversacion.get("status")
                    or "indexed"
                ),
            }
            for etiqueta, valor in metadatos.items():
                if etiqueta == "locator":
                    st.write("**Locator:**")
                    st.json(valor)
                else:
                    st.write(f"**{etiqueta.title()}:** {valor or '—'}")

            with st.expander("🧪 Revisar metadatos", expanded=False):
                st.json({
                    "id": active_id,
                    "titulo": conversacion.get("titulo"),
                    **metadatos,
                })

            st.warning(
                "El índice no contiene el texto completo. Usa el locator "
                "para recuperar la conversación desde su fuente autorizada."
            )

# ============================================
# TAB 5: PLANTILLAS Y REFERENCIAS
# ============================================
with tab5:
    st.subheader("🧩 Plantillas y referencias para integrar")
    st.caption(
        "Patrones externos observados para resolver brechas concretas de CO•RA. "
        "Son referencias; no se copian aplicaciones ni se presupone su licencia."
    )
    catalogo_plantillas = cargar_json_publico(
        "data/plantillas_publicas.json",
        {"templates": []},
    )
    plantillas = catalogo_plantillas.get("templates", [])

    proyectos_por_patron = {
        "inspector de metadatos": ["Rastreador de conversaciones", "Inventario KEEP"],
        "entrega de contexto": ["Memory Bank e HILO", "CO•RA Observer"],
        "catálogo de datos": ["Inventario KEEP", "PDL y GIS"],
        "búsqueda híbrida": ["Rastreador de conversaciones", "Memory Bank e HILO"],
        "búsqueda de conversaciones": ["Rastreador de conversaciones"],
        "catálogo de recursos": ["Inventario KEEP"],
        "visualización geoespacial": ["PDL y GIS"],
        "índice espacial": ["PDL y GIS"],
        "procesamiento geoespacial": ["PDL y GIS"],
        "portal electoral": ["Gestión municipal", "PDL y GIS"],
        "panel de incidentes": ["Gestión municipal", "PDL y GIS"],
        "monitor de disponibilidad": ["CO•RA Observer", "Agentes y evaluación"],
        "flujo de decisión por umbral": ["Agentes y evaluación", "Gestión municipal"],
        "panel de clasificación": ["Agentes y evaluación"],
        "visor comparativo": ["Agentes y evaluación"],
        "calculadora especializada": ["Gestión municipal"],
        "panel de movilidad": ["PDL y GIS"],
        "explorador de viajes": ["PDL y GIS"],
        "estimador": ["Gestión municipal"],
        "coincidencia visual": ["Plantillas e interfaces"],
        "generador de artefactos": ["Plantillas e interfaces"],
        "vista científica rápida": ["Plantillas e interfaces"],
        "simulación interactiva": ["Plantillas e interfaces"],
        "interacción textual": ["Plantillas e interfaces"],
    }

    if plantillas:
        st.markdown("### 👁️ Vista previa y conexión")
        plantilla_previa = st.selectbox(
            "Selecciona una plantilla",
            plantillas,
            format_func=lambda p: p.get("name", "Referencia"),
            key="plantilla_vista_previa",
        )
        categoria_previa = plantilla_previa.get("category", "otra")
        proyectos_conectados = proyectos_por_patron.get(
            categoria_previa,
            ["CO•RA Ecosistema"],
        )
        st.caption(
            "Conecta con: " + " · ".join(proyectos_conectados)
            + f" · Patrón: {categoria_previa}"
        )
        mostrar_previa = st.checkbox(
            "Mostrar sitio incrustado",
            value=True,
            help="Algunos sitios externos pueden impedir la vista incrustada.",
            key="mostrar_vista_plantilla",
        )
        if mostrar_previa:
            st.iframe(
                plantilla_previa.get("url"),
                height=520,
            )
        st.link_button(
            "↗️ Abrir plantilla en otra pestaña",
            plantilla_previa.get("url"),
        )
        st.markdown("---")

    categorias_plantilla = sorted({p.get("category", "otra") for p in plantillas})
    filtro_plantilla = st.multiselect(
        "Filtrar por patrón",
        categorias_plantilla,
        key="filtro_catalogo_plantillas",
    )
    visibles = [
        p for p in plantillas
        if not filtro_plantilla or p.get("category") in filtro_plantilla
    ]
    st.metric("Referencias registradas", len(plantillas))
    for plantilla in visibles:
        with st.container(border=True):
            col_info, col_link = st.columns([4, 1])
            with col_info:
                st.markdown(f"**{plantilla.get('name', 'Referencia')}**")
                st.caption(
                    f"Patrón: {plantilla.get('category', 'por clasificar')} · "
                    f"Prioridad: {plantilla.get('priority', 'por revisar')}"
                )
                conectados = proyectos_por_patron.get(
                    plantilla.get("category"),
                    ["CO•RA Ecosistema"],
                )
                st.caption("Proyectos: " + " · ".join(conectados))
            with col_link:
                st.link_button(
                    "Abrir referencia",
                    plantilla.get("url", "https://streamlit.io/"),
                    use_container_width=True,
                )

# ============================================
# TAB 6: CATÁLOGO DE ACTIVOS
# ============================================
with tab6:
    st.subheader("🗃️ Catálogo de activos y recursos")
    st.caption(
        "Qué existe, para qué sirve, su estado y nivel de acceso. "
        "Los activos privados se representan mediante referencias contextuales."
    )
    catalogo_activos = cargar_json_publico(
        "data/catalogo_activos_publico.json",
        {"assets": []},
    )
    activos = catalogo_activos.get("assets", [])
    tipos_activo = sorted({a.get("type", "otro") for a in activos})
    accesos_activo = sorted({a.get("access", "por_revisar") for a in activos})
    col_tipo, col_acceso = st.columns(2)
    with col_tipo:
        filtro_tipo_activo = st.multiselect(
            "Tipo de activo",
            tipos_activo,
            key="filtro_tipo_activo",
        )
    with col_acceso:
        filtro_acceso_activo = st.multiselect(
            "Nivel de acceso",
            accesos_activo,
            key="filtro_acceso_activo",
        )
    activos_visibles = [
        activo for activo in activos
        if (not filtro_tipo_activo or activo.get("type") in filtro_tipo_activo)
        and (not filtro_acceso_activo or activo.get("access") in filtro_acceso_activo)
    ]
    a1, a2, a3 = st.columns(3)
    a1.metric("Activos registrados", len(activos))
    a2.metric("Públicos o sanitizados", sum(
        1 for activo in activos
        if "público" in activo.get("access", "")
    ))
    a3.metric("Privados o locales", sum(
        1 for activo in activos
        if activo.get("access") in {"privado", "local", "privado_revisable", "privado_sanitizable"}
    ))
    filas_activos = [
        {
            "Activo": activo.get("name"),
            "Tipo": activo.get("type"),
            "Dominio": activo.get("domain", "otro").replace("_", " "),
            "Estado": activo.get("status", "por_revisar").replace("_", " "),
            "Acceso": activo.get("access", "por_revisar").replace("_", " "),
            "Función": activo.get("relation", ""),
        }
        for activo in activos_visibles
    ]
    st.dataframe(filas_activos, use_container_width=True, hide_index=True)

    keep_publico = cargar_json_publico(
        "data/keep_inventarios_publico.json",
        {},
    )
    if keep_publico:
        with st.expander("📝 Notas KEEP e inventario físico", expanded=False):
            st.caption(
                "Resumen numérico y conexiones contextuales. Los títulos, "
                "contenidos y ubicaciones permanecen privados."
            )
            resumen_keep = keep_publico.get("summary", {})
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Notas KEEP", resumen_keep.get("keep_notes", 0))
            k2.metric(
                "Registros físicos",
                resumen_keep.get("physical_inventory_records", 0),
            )
            k3.metric(
                "Familias explícitas",
                resumen_keep.get("explicit_families", 0),
            )
            k4.metric(
                "Familias por revisar",
                resumen_keep.get("candidate_families", 0),
            )
            colecciones_keep = [
                {
                    "Colección": item.get("name"),
                    "Registros": item.get("records"),
                    "Estado": item.get("status", "pendiente").replace("_", " "),
                    "Encaminar a": item.get("route", "revision").replace("_", " "),
                    "Conecta con": " · ".join(item.get("connects_to", [])),
                }
                for item in keep_publico.get("collections", [])
            ]
            st.dataframe(
                colecciones_keep,
                use_container_width=True,
                hide_index=True,
            )

    expediente_documental = cargar_json_publico(
        "data/expediente_documental_publico.json",
        {},
    )
    if expediente_documental:
        with st.expander("📂 Expediente documental contextual", expanded=True):
            st.caption(expediente_documental.get("purpose", ""))
            resumen_documental = expediente_documental.get("summary", {})
            e1, e2, e3, e4 = st.columns(4)
            e1.metric("Archivos revisados", resumen_documental.get("files_reviewed", 0))
            e2.metric("Familias", len(expediente_documental.get("families", [])))
            e3.metric("Duplicados exactos", resumen_documental.get("exact_duplicate_groups", 0))
            e4.metric("Copias redundantes", resumen_documental.get("redundant_copies", 0))

            st.dataframe(
                [
                    {
                        "Familia": familia.get("name", ""),
                        "Estado": familia.get("status", "").replace("_", " "),
                        "Uso como evidencia": familia.get("evidence_use", ""),
                        "Acción pública": familia.get("public_action", ""),
                    }
                    for familia in expediente_documental.get("families", [])
                ],
                width="stretch",
                hide_index=True,
            )

            manifiesto_reciente = expediente_documental.get(
                "latest_manifest_observation", {}
            )
            if manifiesto_reciente:
                st.markdown("**Último manifiesto local observado**")
                l1, l2, l3, l4 = st.columns(4)
                l1.metric("Entradas", manifiesto_reciente.get("entries", 0))
                l2.metric("Archivos", manifiesto_reciente.get("files", 0))
                l3.metric("Carpetas", manifiesto_reciente.get("directories", 0))
                l4.metric(
                    "Copias redundantes",
                    manifiesto_reciente.get("redundant_copies_in_manifest", 0),
                )
                st.caption(manifiesto_reciente.get("interpretation", ""))
                st.dataframe(
                    [
                        {
                            "Familia": ruta.get("family", "").replace("_", " "),
                            "Encaminar a": ruta.get("route", "").replace("_", " "),
                            "Estado": ruta.get("status", "").replace("_", " "),
                        }
                        for ruta in manifiesto_reciente.get("routes", [])
                    ],
                    width="stretch",
                    hide_index=True,
                )

            with st.expander("Candidatos de evidencia y límites", expanded=False):
                for candidato in expediente_documental.get("evidence_candidates", []):
                    st.write(
                        f"- **{candidato.get('candidate', 'Evidencia')}** · "
                        f"{candidato.get('relation', '').replace('_', ' ')} · "
                        f"{candidato.get('status', '').replace('_', ' ')}"
                    )
                st.markdown("**Límites de interpretación**")
                for limite in expediente_documental.get("limitations", []):
                    st.write(f"- {limite}")
    st.info(
        "El catálogo no permite abrir activos privados. La recuperación exige "
        "un localizador autorizado y permanece bajo control local."
    )

# ============================================
# TAB 7: MESA REDONDA
# ============================================
with tab7:
    st.subheader("💬 Mesa Redonda CO•RA")
    mesa = cargar_json_publico("mesa_redonda/router_agentes_v1.json", {"turnos": []})
    metadata = mesa.get("metadata", {})
    st.write(f"**Tema:** {metadata.get('tema', 'Sin tema')}")
    st.write(f"**Estado:** {metadata.get('estado', 'sin estado')}")
    st.caption("Los nuevos turnos se preparan y descargan localmente. Publicarlos requiere revisión humana.")

    for turno in mesa.get("turnos", []):
        with st.expander(f"Turno {turno.get('turno_numero')} · {turno.get('agente')}"):
            st.write(turno.get("resumen", ""))
            if turno.get("pregunta_para_siguiente"):
                st.markdown(f"**Pregunta siguiente:** {turno['pregunta_para_siguiente']}")

    sintesis = mesa.get("sintesis_provisional", {})
    if sintesis:
        st.markdown("### 🧩 Síntesis provisional")
        col_acuerdos, col_preguntas = st.columns(2)
        with col_acuerdos:
            st.markdown("**Acuerdos**")
            for acuerdo in sintesis.get("acuerdos", []):
                st.write(f"- {acuerdo}")
        with col_preguntas:
            st.markdown("**Preguntas abiertas**")
            for pregunta_abierta in sintesis.get("preguntas_abiertas", []):
                st.write(f"- {pregunta_abierta}")

    st.markdown("---")
    st.markdown("### 🧠 Comparación colaborativa")
    st.caption("Una pregunta común, dos perspectivas independientes y una respuesta unificada por el moderador.")

    with st.form("form_comparacion_agentes", clear_on_submit=False):
        pregunta_comun = st.text_area(
            "Pregunta para ambos agentes",
            height=110,
            placeholder="Escribe una sola pregunta para Qwen y ChatGPT."
        )

        col_qwen, col_chatgpt = st.columns(2)
        with col_qwen:
            st.markdown("#### Agente 1 · Qwen")
            respuesta_qwen = st.text_area(
                "Respuesta de Qwen",
                height=260,
                placeholder="Pega aquí la respuesta de Qwen."
            )
        with col_chatgpt:
            st.markdown("#### Agente 2 · ChatGPT")
            respuesta_chatgpt = st.text_area(
                "Respuesta de ChatGPT",
                height=260,
                placeholder="Pega aquí la respuesta de ChatGPT."
            )

        respuesta_unificada = st.text_area(
            "Respuesta unificada de la mesa",
            height=220,
            placeholder="Integra acuerdos, desacuerdos, evidencia y decisión final."
        )
        preparar_comparacion = st.form_submit_button(
            "🧪 Validar y preparar mesa",
            type="primary"
        )

    if preparar_comparacion:
        pregunta_limpia = pregunta_comun.strip()
        qwen_limpia = respuesta_qwen.strip()
        chatgpt_limpia = respuesta_chatgpt.strip()
        unificada_limpia = respuesta_unificada.strip()
        conteos = {
            "qwen": len(qwen_limpia.split()),
            "chatgpt": len(chatgpt_limpia.split()),
            "unificada": len(unificada_limpia.split())
        }
        errores_mesa = []

        if not pregunta_limpia:
            errores_mesa.append("Escribe la pregunta común.")
        if not qwen_limpia:
            errores_mesa.append("Falta la respuesta de Qwen.")
        if not chatgpt_limpia:
            errores_mesa.append("Falta la respuesta de ChatGPT.")
        if not unificada_limpia:
            errores_mesa.append("Falta la respuesta unificada.")
        for agente_nombre, total_palabras in conteos.items():
            if total_palabras > 800:
                errores_mesa.append(
                    f"La respuesta {agente_nombre} tiene {total_palabras} palabras; el máximo es 800."
                )

        if errores_mesa:
            for error_mesa in errores_mesa:
                st.error(error_mesa)
            st.session_state.pop("comparacion_borrador", None)
        else:
            st.session_state.comparacion_borrador = {
                "tipo": "mesa_redonda_comparativa",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "pregunta": pregunta_limpia,
                "agentes": {
                    "qwen": {
                        "respuesta": qwen_limpia,
                        "conteo_palabras": conteos["qwen"]
                    },
                    "chatgpt": {
                        "respuesta": chatgpt_limpia,
                        "conteo_palabras": conteos["chatgpt"]
                    }
                },
                "respuesta_unificada": unificada_limpia,
                "conteo_palabras_unificada": conteos["unificada"],
                "moderador": "Jorge Hernández",
                "estado": "borrador_pendiente_revision"
            }

    comparacion = st.session_state.get("comparacion_borrador")
    if comparacion:
        st.success("Mesa comparativa válida y lista para revisión.")
        st.json(comparacion)
        st.download_button(
            "⬇️ Descargar mesa JSON",
            data=json.dumps(comparacion, indent=2, ensure_ascii=False),
            file_name="mesa_redonda_comparativa.json",
            mime="application/json"
        )
        st.warning("La descarga no publica las respuestas ni las envía a ningún agente.")

# ============================================
# TAB 8: SEGUIMIENTO DE ACTIVIDADES
# ============================================
with tab8:
    st.subheader("✅ Dashboard de seguimiento de actividades")
    st.caption(
        "Matriz operativa conectada con proyectos, compromisos, capas de "
        "contexto y evidencia de cierre. Una actividad no equivale a un proyecto."
    )

    matriz_actividades = cargar_json_publico(
        "data/actividades_seguimiento.json",
        {"activities": []},
    )
    actividades = matriz_actividades.get("activities", [])

    if not actividades:
        st.info("Todavía no hay actividades registradas en la matriz de organización.")
    else:
        estados = sorted({item.get("state", "sin_estado") for item in actividades})
        prioridades = sorted({item.get("priority", "sin_prioridad") for item in actividades})
        proyectos_actividad = sorted({item.get("project", "Sin proyecto") for item in actividades})
        capas = sorted({int(item.get("layer", 0)) for item in actividades})

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            filtro_estados = st.multiselect(
                "Estado",
                estados,
                default=estados,
                format_func=lambda valor: valor.replace("_", " ").title(),
                key="seguimiento_estados",
            )
        with f2:
            filtro_prioridades = st.multiselect(
                "Prioridad",
                prioridades,
                default=prioridades,
                format_func=lambda valor: valor.title(),
                key="seguimiento_prioridades",
            )
        with f3:
            filtro_proyectos = st.multiselect(
                "Proyecto",
                proyectos_actividad,
                default=proyectos_actividad,
                key="seguimiento_proyectos",
            )
        with f4:
            filtro_capas = st.multiselect(
                "Capa",
                capas,
                default=capas,
                format_func=lambda valor: f"Capa {valor}",
                key="seguimiento_capas",
            )

        actividades_visibles = [
            item for item in actividades
            if item.get("state", "sin_estado") in filtro_estados
            and item.get("priority", "sin_prioridad") in filtro_prioridades
            and item.get("project", "Sin proyecto") in filtro_proyectos
            and int(item.get("layer", 0)) in filtro_capas
        ]

        total_actividades = len(actividades_visibles)
        en_movimiento = sum(
            1 for item in actividades_visibles
            if item.get("state") in {"en_curso", "en_revision"}
        )
        completadas = sum(
            1 for item in actividades_visibles
            if item.get("state") == "completada"
        )
        alta_prioridad = sum(
            1 for item in actividades_visibles
            if item.get("priority") == "alta"
            and item.get("state") != "completada"
        )
        avance_promedio = round(
            sum(int(item.get("progress", 0)) for item in actividades_visibles)
            / max(total_actividades, 1)
        )

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Actividades", total_actividades)
        k2.metric("En movimiento", en_movimiento)
        k3.metric("Completadas", completadas)
        k4.metric("Prioridad alta abierta", alta_prioridad)
        k5.metric("Avance promedio", f"{avance_promedio}%")
        st.progress(avance_promedio / 100)
        st.caption(
            "Fuente: " + matriz_actividades.get("source_of_truth", "sin fuente")
            + " · Actualización: " + matriz_actividades.get("updated_at", "sin fecha")
            + " · Unidad: " + matriz_actividades.get("grain", "actividad")
        )

        if actividades_visibles:
            conteo_estados = {
                estado: sum(
                    1 for item in actividades_visibles
                    if item.get("state") == estado
                )
                for estado in estados
            }
            conteo_capas = {
                capa: sum(
                    1 for item in actividades_visibles
                    if int(item.get("layer", 0)) == capa
                )
                for capa in capas
            }

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Distribución por estado")
                st.bar_chart(
                    {
                        "Estado": [clave.replace("_", " ").title() for clave in conteo_estados],
                        "Actividades": list(conteo_estados.values()),
                    },
                    x="Estado",
                    y="Actividades",
                    color="#21618C",
                )
            with c2:
                st.markdown("#### Distribución por capa de contexto")
                st.bar_chart(
                    {
                        "Capa": [f"Capa {clave}" for clave in conteo_capas],
                        "Actividades": list(conteo_capas.values()),
                    },
                    x="Capa",
                    y="Actividades",
                    color="#1E8449",
                )

            st.markdown("#### Próximas actividades prioritarias")
            orden_prioridad = {"alta": 0, "media": 1, "baja": 2}
            proximas = sorted(
                [item for item in actividades_visibles if item.get("state") != "completada"],
                key=lambda item: (
                    orden_prioridad.get(item.get("priority", "baja"), 3),
                    -int(item.get("progress", 0)),
                    item.get("id", ""),
                ),
            )[:3]
            for item in proximas:
                with st.container(border=True):
                    st.markdown(
                        f"**{item.get('title', 'Actividad')}** · "
                        f"{item.get('priority', 'sin prioridad').title()}"
                    )
                    st.caption(
                        f"{item.get('project', 'Sin proyecto')} · "
                        f"Capa {item.get('layer', 0)} · "
                        f"{item.get('state', 'sin estado').replace('_', ' ')}"
                    )
                    st.progress(int(item.get("progress", 0)) / 100)
                    st.write("**Siguiente acción:** " + item.get("next_action", ""))
                    st.write(
                        "**Cierre verificable:** "
                        + item.get("completion_evidence", "")
                    )
                    metodologia = item.get("methodology", {})
                    requisitos = item.get("requirements", {})
                    if metodologia or requisitos:
                        with st.expander("Metodología, alcance y bloqueos", expanded=True):
                            if requisitos:
                                st.write(
                                    f"**Checklist:** {requisitos.get('checklist_id', '')} · "
                                    f"{requisitos.get('closed', 0)}/{requisitos.get('total', 0)} cerrados · "
                                    f"{requisitos.get('pending', 0)} pendientes · "
                                    f"{requisitos.get('objectives', 0)} objetivos"
                                )
                                st.markdown("**Bloqueos críticos**")
                                for bloqueo in requisitos.get("critical_open", []):
                                    st.write(f"- {bloqueo}")
                            if metodologia:
                                if metodologia.get("structural_principle"):
                                    st.markdown("**Principio de excavación estructural**")
                                    st.write(metodologia["structural_principle"])
                                    st.caption(" → ".join(metodologia.get("depth_route", [])))
                                st.markdown("**Secuencia de trabajo**")
                                st.write(" → ".join(metodologia.get("sequence", [])))
                                st.markdown("**Hallazgos**")
                                for hallazgo in metodologia.get("findings", []):
                                    st.write(f"- {hallazgo}")
                                st.markdown("**Alcance**")
                                st.write(" · ".join(metodologia.get("scope", [])))
                                st.markdown("**Problemáticas**")
                                for problema in metodologia.get("problems", []):
                                    st.write(f"- {problema}")
                                if metodologia.get("project_narrative_fields"):
                                    st.markdown("**Semblanza profesional del proyecto**")
                                    st.write(" · ".join(metodologia["project_narrative_fields"]))
                                if metodologia.get("professional_premise"):
                                    st.info(metodologia["professional_premise"])
                                st.caption(metodologia.get("privacy_rule", ""))

            st.markdown("#### Matriz completa de actividades")
            st.dataframe(
                [
                    {
                        "ID": item.get("id", ""),
                        "Actividad": item.get("title", ""),
                        "Proyecto": item.get("project", ""),
                        "Capa": item.get("layer", 0),
                        "Etapa": item.get("stage", "").replace("_", " "),
                        "Prioridad": item.get("priority", "").title(),
                        "Estado": item.get("state", "").replace("_", " "),
                        "Avance": f"{item.get('progress', 0)}%",
                        "Evidencia": item.get("evidence_status", "").replace("_", " "),
                        "Siguiente acción": item.get("next_action", ""),
                    }
                    for item in actividades_visibles
                ],
                width="stretch",
                hide_index=True,
            )

            st.download_button(
                "⬇️ Descargar matriz de actividades",
                data=json.dumps(matriz_actividades, indent=2, ensure_ascii=False),
                file_name="cora_actividades_seguimiento.json",
                mime="application/json",
            )
        else:
            st.warning("Los filtros actuales no devuelven actividades.")

# ============================================
# TAB 9: PRESENTACIÓN INMERSIVA
# ============================================
with tab9:
    st.subheader("🎞️ Presentación inmersiva del proyecto")
    st.caption(
        "Una demo narrativa e interactiva que cruza proyectos, actividades, activos, trayectoria e índice de conversaciones para mostrar la visión en tiempo real."
    )
    render_presentacion_inmersiva(
        PROYECTOS_PUBLICOS,
        ACTIVIDADES_PUBLICAS,
        ACTIVOS_PUBLICOS,
        TRAYECTORIA_PUBLICA,
        INDICE_CONVERSACIONES_PUBLICO,
    )

    st.divider()
    st.subheader("🗺️ PDL localizado · demo y ruta de desarrollo")
    st.caption(
        "Esta vista usa únicamente metadatos sanitizados del rastreo local. "
        "No intenta abrir carpetas privadas desde la aplicación pública."
    )
    inventario_pdl = cargar_json_publico(
        "data/pdl_demo_inventario_publico.json",
        {
            "canonical_demo_candidate": {},
            "verification": {},
            "surfaces": [],
            "documented_data_contracts": [],
            "local_asset_families": [],
            "development_opportunities": [],
            "integration_decision": {},
            "public_privacy_rules": [],
        },
    )

    candidato_demo = inventario_pdl.get("canonical_demo_candidate", {})
    superficies_pdl = inventario_pdl.get("surfaces", [])
    oportunidades_pdl = inventario_pdl.get("development_opportunities", [])
    verificacion_pdl = inventario_pdl.get("verification", {})

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Revisiones ZIP", candidato_demo.get("archive_revision_count", 0))
    p2.metric("Archivos del candidato", candidato_demo.get("unpacked_file_count", 0))
    p3.metric("Superficies", len(superficies_pdl))
    p4.metric("Líneas desarrollables", len(oportunidades_pdl))
    st.info(
        "Candidato canónico provisional: "
        + candidato_demo.get("name", "sin candidato")
        + " · Estado: "
        + candidato_demo.get("status", "sin estado").replace("_", " ")
    )

    pdl_tab1, pdl_tab2, pdl_tab3, pdl_tab4 = st.tabs(
        [
            "Recorrido del demo",
            "Qué puedo desarrollar",
            "Activos y fuentes",
            "Verificación y publicación",
        ]
    )

    with pdl_tab1:
        paquete_pdl_dir = BASE_DIR / "data" / "pdl_demo"
        manifiesto_demo = cargar_json_publico(
            str(paquete_pdl_dir / "manifest.json"),
            {"layers": [], "population": {}, "privacy": {}},
        )
        archivos_demo = {
            "Límite municipal": "limite_municipal.geojson",
            "Localidades": "localidades_poblacion.geojson",
            "Colonias": "colonias.geojson",
            "Secciones": "secciones_46.geojson",
        }
        capas_geojson = {
            nombre: cargar_json_publico(
                str(paquete_pdl_dir / archivo),
                {"type": "FeatureCollection", "features": []},
            )
            for nombre, archivo in archivos_demo.items()
        }

        st.markdown("#### Territorio interactivo")
        st.caption(
            "Activa y desactiva capas, toca una geometría y compara su contexto. "
            "La población se muestra como dato agregado, no como ubicación de personas."
        )
        capas_activas = st.multiselect(
            "Capas visibles",
            list(archivos_demo),
            default=["Límite municipal", "Localidades", "Secciones"],
            key="pdl_capas_visibles",
        )

        estilos_pdl = {
            "Límite municipal": {
                "fill": [12, 22, 35, 18],
                "line": [72, 224, 196, 235],
                "width": 4,
            },
            "Localidades": {
                "fill": [24, 182, 155, 82],
                "line": [111, 245, 218, 220],
                "width": 2,
            },
            "Colonias": {
                "fill": [244, 114, 182, 62],
                "line": [249, 168, 212, 210],
                "width": 2,
            },
            "Secciones": {
                "fill": [56, 189, 248, 25],
                "line": [125, 211, 252, 185],
                "width": 1,
            },
        }
        capas_deck = []
        for nombre_capa in capas_activas:
            estilo = estilos_pdl[nombre_capa]
            capas_deck.append(
                pdk.Layer(
                    "GeoJsonLayer",
                    data=capas_geojson[nombre_capa],
                    id=f"pdl-{nombre_capa.lower().replace(' ', '-')}",
                    pickable=nombre_capa != "Límite municipal",
                    stroked=True,
                    filled=True,
                    get_fill_color=estilo["fill"],
                    get_line_color=estilo["line"],
                    get_line_width=estilo["width"],
                    line_width_min_pixels=estilo["width"],
                    auto_highlight=True,
                    highlight_color=[255, 190, 80, 180],
                )
            )

        if capas_deck:
            st.pydeck_chart(
                pdk.Deck(
                    layers=capas_deck,
                    initial_view_state=pdk.ViewState(
                        latitude=18.89,
                        longitude=-100.26,
                        zoom=9.55,
                        pitch=22,
                        bearing=0,
                    ),
                    map_style="light",
                    tooltip={
                        "html": (
                            "<b>{nombre}</b><br/>"
                            "Población: {poblacion_total}<br/>"
                            "Participación municipal: {pct_total_municipal}%<br/>"
                            "Sección: {seccion}<br/>"
                            "CP: {cp}<br/>"
                            "Área: {area_ha} ha"
                        ),
                        "style": {
                            "backgroundColor": "#0b1727",
                            "color": "#f8fafc",
                            "fontSize": "13px",
                        },
                    },
                ),
                use_container_width=True,
                height=570,
            )
        else:
            st.info("Selecciona al menos una capa para visualizar el territorio.")

        st.markdown(
            "**Leyenda:** 🟩 localidades · 🟦 secciones · 🩷 colonias · "
            "borde turquesa: límite municipal"
        )

        localidades_demo = capas_geojson.get("Localidades", {}).get("features", [])
        localidades_por_nombre = {
            feature.get("properties", {}).get("nombre", "Sin nombre"): feature.get(
                "properties", {}
            )
            for feature in localidades_demo
        }
        if localidades_por_nombre:
            localidad_activa = st.selectbox(
                "Toca los datos desde una localidad",
                sorted(localidades_por_nombre),
                key="pdl_localidad_activa",
            )
            ficha_localidad = localidades_por_nombre[localidad_activa]
            f1, f2, f3 = st.columns(3)
            f1.metric(
                "Población registrada",
                f"{int(ficha_localidad.get('poblacion_total', 0)):,}",
            )
            f2.metric(
                "Participación municipal",
                f"{float(ficha_localidad.get('pct_total_municipal', 0)):.2f}%",
            )
            f3.metric(
                "Área del polígono",
                f"{float(ficha_localidad.get('area_ha', 0)):.2f} ha",
            )
            with st.expander("Ver ficha y trazabilidad de la localidad"):
                st.json(ficha_localidad)

        resumen_capas = manifiesto_demo.get("layers", [])
        m1, m2, m3 = st.columns(3)
        m1.metric(
            "Geometrías publicables",
            sum(int(item.get("features", 0)) for item in resumen_capas),
        )
        m2.metric(
            "Población municipal de referencia",
            f"{int(manifiesto_demo.get('population', {}).get('population_sum', 0)):,}",
        )
        m3.metric("Sistema espacial", manifiesto_demo.get("crs", "Sin definir"))
        st.warning(
            "Estado de evidencia: las geometrías fueron validadas localmente y "
            "sanitizadas, pero su localizador de fuente primaria aún debe fijarse "
            "antes de una publicación institucional."
        )

        if superficies_pdl:
            superficie_ids = [item.get("id", "") for item in superficies_pdl]
            superficie_activa = st.selectbox(
                "Superficie a explorar",
                superficie_ids,
                format_func=lambda surface_id: next(
                    (
                        item.get("name", surface_id)
                        for item in superficies_pdl
                        if item.get("id") == surface_id
                    ),
                    surface_id,
                ),
                key="pdl_superficie_demo",
            )
            detalle_superficie = next(
                (
                    item
                    for item in superficies_pdl
                    if item.get("id") == superficie_activa
                ),
                {},
            )
            with st.container(border=True):
                st.markdown(f"### {detalle_superficie.get('name', 'Superficie PDL')}")
                st.code(detalle_superficie.get("route", "/"), language=None)
                st.write(detalle_superficie.get("purpose", ""))
                st.write("**Interacción:** " + detalle_superficie.get("interaction", ""))
                st.write("**Estado de datos:** " + detalle_superficie.get("data_state", ""))
                st.caption(
                    "Preparación: "
                    + detalle_superficie.get("readiness", "sin estado").replace("_", " ")
                )

        st.markdown("#### Contratos de datos documentados")
        st.dataframe(
            to_simple_table(
                inventario_pdl.get("documented_data_contracts", []),
                ["source", "coverage", "join_key", "source_crs", "target_crs", "note"],
            ),
            use_container_width=True,
            hide_index=True,
        )

    with pdl_tab2:
        st.write(
            "Las oportunidades se ordenan por capacidad de reutilizar lo ya localizado "
            "y producir un piloto verificable con el menor esfuerzo adicional."
        )
        st.dataframe(
            to_simple_table(
                oportunidades_pdl,
                [
                    "priority",
                    "name",
                    "deliverable",
                    "reuse",
                    "first_pilot",
                    "status",
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

    with pdl_tab3:
        st.dataframe(
            to_simple_table(
                inventario_pdl.get("local_asset_families", []),
                ["family", "examples", "role", "deduplication"],
            ),
            use_container_width=True,
            hide_index=True,
        )

    with pdl_tab4:
        v1, v2 = st.columns(2)
        with v1:
            st.markdown("#### Confirmado directamente")
            for item in verificacion_pdl.get("directly_verified", []):
                st.write(f"- {item}")
            st.markdown("#### Documentado, no reejecutado")
            for item in verificacion_pdl.get("documented_but_not_reexecuted", []):
                st.write(f"- {item}")
        with v2:
            st.markdown("#### Pendiente antes de publicar")
            for item in verificacion_pdl.get("pending_before_public_release", []):
                st.write(f"- {item}")
            st.markdown("#### Reglas de privacidad")
            for item in inventario_pdl.get("public_privacy_rules", []):
                st.write(f"- {item}")

        decision_integracion = inventario_pdl.get("integration_decision", {})
        st.warning(decision_integracion.get("deferred_action", ""))
        st.write("**Ahora:** " + decision_integracion.get("current_action", ""))
        st.caption(decision_integracion.get("reason", ""))

    st.download_button(
        "⬇️ Descargar inventario PDL sanitizado",
        data=json.dumps(inventario_pdl, indent=2, ensure_ascii=False),
        file_name="pdl_demo_inventario_publico.json",
        mime="application/json",
        key="descargar_inventario_pdl",
    )

# ============================================
# TAB 10: ANALIZADOR MAESTRO DE PROYECTOS POTENCIALES
# ============================================
with tab10:
    st.subheader("🧮 Analizador maestro de proyectos potenciales")
    st.caption(
        "Matriz sanitizada para separar núcleo madre, proyectos vivos, evidencia, "
        "red de contactos, soporte técnico y temporales sin mezclar capas."
    )
    analizador = cargar_json_publico(
        "data/analizador_proyectos_potenciales_publico.json",
        {
            "summary": {},
            "layers": [],
            "projects": [],
            "duplicate_groups": [],
            "ingested_sources": [],
            "discovered_title_candidates": [],
            "claim_validation_queue": [],
            "contradiction_queue": [],
        },
    )

    if analizador:
        resumen_analizador = analizador.get("summary", {})
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Núcleo", resumen_analizador.get("core_nucleus", 0))
        c2.metric("Vivos", resumen_analizador.get("projects_vivos", 0))
        c3.metric("Evidencia", resumen_analizador.get("evidence_profesional", 0))
        c4.metric("Contactos", resumen_analizador.get("red_contactos", 0))
        c5.metric("Soporte", resumen_analizador.get("soporte_tecnico_multimedia", 0))
        c6.metric("Temporales", resumen_analizador.get("temporales_descartables", 0))

        st.markdown("#### Resumen ejecutivo")
        st.write(
            "Vale la pena seguir: CO•RA, PDL/GIS, Radar PDL, red profesional, "
            "portafolio basado en evidencia, inventario KEEP y el material de soporte."
        )
        st.write(
            "Duplicados principales: familias MACROS, CURRICULUM, PDL territorial, "
            "variantes de semblanza/presentación y paquetes de contactos por chat."
        )
        st.write(
            "Evidencia: presentaciones, semblanzas, CV, documentos PDL, material municipal "
            "y archivos que prueban trayectoria o entregables."
        )
        st.write(
            "Soporte: demos HTML, widgets, instaladores, capturas y material multimedia."
        )
        st.write(
            "Temporales: pendientes de revisión y contenedores de descarte controlado."
        )

        st.markdown("#### Capas")
        st.dataframe(
            to_simple_table(
                analizador.get("layers", []),
                ["id", "name", "description"],
            ),
            use_container_width=True,
            hide_index=True,
        )

        con_filtro1, con_filtro2, con_filtro3 = st.columns(3)
        with con_filtro1:
            filtro_categoria = st.multiselect(
                "Categoría principal",
                sorted({item.get("primary_category", "sin_categoria") for item in analizador.get("projects", [])}),
                default=[],
                key="filtro_analizador_categoria",
            )
        with con_filtro2:
            filtro_estado = st.multiselect(
                "Estado",
                sorted({item.get("status", "sin_estado") for item in analizador.get("projects", [])}),
                default=[],
                key="filtro_analizador_estado",
            )
        with con_filtro3:
            filtro_relacion = st.text_input(
                "Filtrar por relación",
                placeholder="CO•RA, PDL, contacto, evidencia...",
                key="filtro_analizador_relacion",
            ).strip().lower()

        proyectos_analizador = analizador.get("projects", [])
        if filtro_categoria:
            proyectos_analizador = [
                item for item in proyectos_analizador
                if item.get("primary_category") in filtro_categoria
            ]
        if filtro_estado:
            proyectos_analizador = [
                item for item in proyectos_analizador
                if item.get("status") in filtro_estado
            ]
        if filtro_relacion:
            proyectos_analizador = [
                item for item in proyectos_analizador
                if filtro_relacion in " ".join([
                    str(item.get("name", "")),
                    str(item.get("relation", "")),
                    str(item.get("associated_contact_or_project", "")),
                    str(item.get("source_hint", "")),
                    str(item.get("next_action", "")),
                ]).lower()
            ]

        st.metric("Entradas visibles", len(proyectos_analizador))
        st.dataframe(
            to_simple_table(
                proyectos_analizador,
                [
                    "name",
                    "primary_category",
                    "layer",
                    "type",
                    "value",
                    "status",
                    "duplicate_state",
                    "relation",
                    "associated_contact_or_project",
                    "next_action",
                    "confidence",
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Duplicados y familias")
        st.dataframe(
            to_simple_table(
                analizador.get("duplicate_groups", []),
                ["group_key", "label", "members", "status"],
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Fuentes incorporadas")
        st.caption(
            "Una conversación de IA ayuda a descubrir candidatos, pero se conserva "
            "como fuente derivada hasta relacionarla con documentos o entregables verificables."
        )
        st.dataframe(
            to_simple_table(
                analizador.get("ingested_sources", []),
                [
                    "title",
                    "source_type",
                    "captured_at",
                    "evidence_level",
                    "privacy",
                    "use",
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

        candidatos_titulo = analizador.get("discovered_title_candidates", [])
        st.markdown("#### Títulos rastreados por confirmar")
        st.caption(
            "El título demuestra que existe una referencia localizable, pero no confirma "
            "todavía el contenido, alcance ni estado del proyecto."
        )
        st.metric("Títulos candidatos", len(candidatos_titulo))
        st.dataframe(
            to_simple_table(
                candidatos_titulo,
                [
                    "display_title",
                    "candidate_type",
                    "relation",
                    "status",
                    "confidence",
                    "next_action",
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Cola de validación")
        st.caption(
            "Estas afirmaciones no se publican como hechos confirmados hasta vincular "
            "la evidencia primaria sugerida."
        )
        st.dataframe(
            to_simple_table(
                analizador.get("claim_validation_queue", []),
                ["topic", "claim", "status", "suggested_evidence"],
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Contradicciones en cuarentena")
        st.caption(
            "Las mezclas de perfil o afirmaciones incompatibles quedan aisladas y no "
            "modifican la trayectoria canónica."
        )
        st.dataframe(
            to_simple_table(
                analizador.get("contradiction_queue", []),
                [
                    "topic",
                    "reported_claim",
                    "conflicts_with",
                    "status",
                    "resolution_action",
                ],
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Descargar matriz maestra de proyectos potenciales",
            data=json.dumps(analizador, indent=2, ensure_ascii=False),
            file_name="analizador_proyectos_potenciales_publico.json",
            mime="application/json",
            use_container_width=False,
        )

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("CO•RA Ecosistema Cognitivo Inclusivo · Ente56298 · 2026")
