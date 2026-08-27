"""
CO•RA Tutor — Trayectoria Adaptativa de Aprendizaje
Versión 2.0: 8 áreas + Rastreo de contextos + GitHub Bridge
"""
import streamlit as st
import requests
import json
import hashlib
import base64
from datetime import datetime, timezone
from pathlib import Path

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
# ÁREAS DE CONOCIMIENTO (8 áreas)
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
    """Carga las conversaciones extraídas"""
    ruta = Path("data/conversaciones_extraidas.json")
    if ruta.exists():
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def cargar_json_publico(ruta: str, valor_por_defecto):
    """Carga un artefacto público versionado sin exponer datos locales."""
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return valor_por_defecto

# ============================================
# INTERFAZ PRINCIPAL
# ============================================
st.title("🧭 CO•RA Tutor")
st.markdown("### Trayectoria adaptativa de aprendizaje")
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
    st.write("✅ Rastreo de contextos")
    st.write("✅ 8 áreas de conocimiento")
    st.write("✅ Catálogo público de agentes")
    st.write("✅ Mesa redonda colaborativa")
    st.write("⚠️ Escritura en Memory Bank desactivada" if not ENABLE_GITHUB_WRITES else "✅ Escritura privada habilitada")

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Explorar Área",
    "📚 Historial ChatGPT",
    "🧠 Memory Bank",
    "🤝 Agentes",
    "💬 Mesa Redonda"
])

# ============================================
# TAB 1: EXPLORAR ÁREA
# ============================================
with tab1:
    st.subheader("📋 Contexto Inicial")

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
    st.subheader("🎯 Selecciona un área para explorar")
    
    # Mostrar 8 áreas como botones
    cols = st.columns(4)
    areas_lista = list(AREAS_CONOCIMIENTO.items())
    
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
        area = AREAS_CONOCIMIENTO[area_id]
        
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
                            "respuesta_ejecucion": respuesta_ejecucion
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
# TAB 2: HISTORIAL CHATGPT
# ============================================
with tab2:
    st.subheader("📚 Historial de Conversaciones ChatGPT")
    st.caption("Contextos previos detectados de tu trayectoria de aprendizaje")
    
    conversaciones = cargar_conversaciones()
    
    if conversaciones:
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversaciones", len(conversaciones))
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
        
        st.markdown(f"**{len(conversaciones_filtradas)} conversaciones encontradas**")
        
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
# TAB 4: CATÁLOGO PÚBLICO DE AGENTES
# ============================================
with tab4:
    st.subheader("🤝 Catálogo público de agentes")
    st.caption("Capacidades observadas y pendientes de validación; no ejecuta ni envía tareas.")
    catalogo = cargar_json_publico("data/catalogo_agentes_publico.json", {"agents": []})
    for agente in catalogo.get("agents", []):
        with st.expander(f"{agente.get('display_name', agente.get('agent_id'))} · {agente.get('status', 'sin estado')}"):
            st.write(f"**Acceso:** {agente.get('access_method', 'por definir')}")
            st.write("**Capacidades:**")
            for capacidad in agente.get("capabilities", []):
                st.write(f"- {capacidad}")
    st.info("El despacho automático está desactivado y todo envío externo requiere aprobación humana.")

# ============================================
# TAB 5: MESA REDONDA
# ============================================
with tab5:
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
