"""
CO•RA Tutor — Trayectoria Adaptativa de Aprendizaje
Versión 2.2: Mapa de avances + Mapa abierto + Rastreo de contextos + GitHub Bridge
"""
import streamlit as st
import requests
import json
import hashlib
import base64
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

# ============================================
# AMPLIAR ÁREAS DESDE CATÁLOGO EXTERNO
# ============================================
AREAS_EXTRA = cargar_json_publico(
    "data/areas_conocimiento.json",
    {}
)

AREAS_CONOCIMIENTO.update(AREAS_EXTRA)










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

# Tabs principales
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎯 Trayectoria y proyectos",
    "📚 Conversaciones y registros",
    "🧠 Memoria y contexto",
    "🤝 Agentes y evaluación",
    "🧩 Plantillas y referencias",
    "🗃️ Activos y recursos",
    "💬 Mesa colaborativa"
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

        with st.expander("🔄 Capacidades transferibles y revisión", expanded=False):
            st.markdown("**Capacidades transferibles**")
            for capacidad in trayectoria_profesional.get("transferable_capabilities", []):
                st.write(f"- {capacidad}")
            st.markdown("**Antes de publicar como perfil profesional**")
            for pendiente in trayectoria_profesional.get("review_pending", []):
                st.write(f"- {pendiente}")

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

        for conv in lista:
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
# FOOTER
# ============================================
st.markdown("---")
st.caption("CO•RA Ecosistema Cognitivo Inclusivo · Ente56298 · 2026")
