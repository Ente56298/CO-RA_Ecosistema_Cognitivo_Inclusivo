# 🎬 Generador Automático de Videos CO•RA

## 🎯 Propósito

Sistema completo de 6 fases para generar videos educativos automáticamente usando únicamente fuentes oficiales verificadas (.gov, .edu, organismos internacionales).

## 🚀 Flujo Completo de 6 Fases

### **FASE 0** - Investigación Oficial 🔍
- Consulta solo dominios verificados (.gov, .edu, .who.int, etc.)
- Extrae datos relevantes al tema
- Guarda fuentes en `fuentes.csv`

### **FASE 1** - Guion 📝
- Redacta usando solo datos oficiales
- Formato audiovisual breve (4-8 escenas)
- Máximo 120 palabras, tono educativo

### **FASE 2** - Storyboard 🎨
- 1 línea descriptiva por escena
- Optimizado para generación visual

### **FASE 3** - Generación Visual 🖼️
- Crea imágenes 1080p coherentes
- Una imagen por escena usando DALL-E
- Estilo profesional y educativo

### **FASE 4** - Locución TTS 🎤
- Voz natural clara en MP3
- Velocidad optimizada para accesibilidad
- Calidad HD

### **FASE 5** - Edición y Montaje 🎬
- Sincroniza imágenes y audio
- Añade música de fondo (opcional)
- Normalización de audio

### **FASE 6** - Exportación Final 📦
- `video_final.mp4` listo para publicar
- `fuentes.csv` con referencias verificadas
- `plan.json` con guion y storyboard

## 🛠️ Instalación

### 1. Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configuración
```bash
# Copiar archivo de configuración
cp config/.env.example .env

# Editar con tu API key de OpenAI
nano .env
```

### 3. Variables Requeridas
```env
OPENAI_API_KEY=tu_api_key_aqui
```

### 4. Variables Opcionales
```env
BGMUSIC_PATH=./music/background.mp3
OFFICIAL_DOMAINS=.gov,.edu,.who.int,.un.org
```

## 🚀 Uso

### **Ejecución Rápida**
```bash
python scripts/ejecutar_generador.py "Impacto del cambio climático en México 2025"
```

### **Ejecución Interactiva**
```bash
python scripts/ejecutar_generador.py
# Te pedirá el tema interactivamente
```

### **Ejecución Directa**
```python
from scripts.autopilot_oficial_video import autopilot_video_generator

# Generar video sobre un tema específico
success = autopilot_video_generator("Avances en IA educativa 2025")
```

## 📊 Resultados Generados

### **Archivos de Salida** (carpeta `output/`)
- `video_final.mp4` - Video completo listo para publicar
- `fuentes.csv` - Fuentes oficiales verificadas
- `plan.json` - Guion y storyboard detallado
- `voz.mp3` - Audio de locución
- `scene_01.png`, `scene_02.png`, etc. - Imágenes generadas

### **Ejemplo de fuentes.csv**
```csv
fuente,dato,fecha_consulta,verificado
https://www.who.int,Datos sobre cambio climático y salud...,2024-01-15T10:30:00,True
https://www.gob.mx,Políticas ambientales de México...,2024-01-15T10:31:00,True
```

### **Ejemplo de plan.json**
```json
{
  "script": "El cambio climático representa uno de los mayores desafíos...",
  "scenes": [
    {"n": 1, "visual": "Gráfico mostrando temperaturas globales en aumento"},
    {"n": 2, "visual": "Mapa de México con zonas afectadas por sequía"}
  ]
}
```

## 🔧 Configuración Avanzada

### **Dominios Oficiales Personalizados**
```env
OFFICIAL_DOMAINS=.gov,.edu,.who.int,.un.org,.worldbank.org,.gob.mx,.inegi.org.mx
```

### **Música de Fondo**
```env
BGMUSIC_PATH=./music/background.mp3
```

### **Configuración de TTS**
```env
TTS_VOICE=nova
TTS_SPEED=0.9
```

## 🎯 Ejemplos de Temas

### **Educación**
- "Estadísticas de educación superior en México 2025"
- "Políticas de inclusión digital en América Latina"
- "Avances en inteligencia artificial educativa"

### **Salud**
- "Impacto del cambio climático en la salud pública"
- "Estadísticas de salud mental post-pandemia"
- "Políticas de salud digital en México"

### **Economía**
- "Indicadores económicos de México 2025"
- "Impacto de la digitalización en el empleo"
- "Políticas de desarrollo sostenible"

## 🛡️ Principios de Verificación

### **Solo Fuentes Oficiales**
- Dominios gubernamentales (.gov, .gob.mx)
- Instituciones educativas (.edu)
- Organismos internacionales (WHO, UN, World Bank)
- Institutos estadísticos oficiales (INEGI)

### **Proceso de Verificación**
1. Validación de dominio oficial
2. Extracción de contenido relevante
3. Registro de fuente y fecha
4. Marcado como verificado

## 🌐 Integración CO•RA

### **Valores del Ecosistema**
- **Inclusión**: Videos accesibles con velocidad optimizada
- **Verificación**: Solo fuentes oficiales confiables
- **Educación**: Contenido educativo de calidad
- **Automatización**: Proceso completamente automatizado

### **Compatibilidad**
- Integrable con otros módulos CO•RA
- Salida estándar en formatos universales
- API simple para integración externa

## 📈 Métricas de Calidad

### **Verificación de Fuentes**
- 100% fuentes oficiales verificadas
- Registro completo de referencias
- Trazabilidad de datos

### **Calidad Técnica**
- Video 1080p a 30fps
- Audio HD normalizado
- Duración optimizada (2-5 minutos)

## 🔧 Solución de Problemas

### **Error: API Key no válida**
```bash
# Verificar configuración
cat .env | grep OPENAI_API_KEY
```

### **Error: No se encontraron fuentes**
- Verificar conexión a internet
- Comprobar acceso a sitios oficiales
- Ajustar palabras clave del tema

### **Error: Generación de imágenes**
- Verificar créditos de OpenAI
- Simplificar descripciones visuales
- Revisar políticas de contenido

---

*Generador automático de videos educativos para el ecosistema CO•RA* 🎬