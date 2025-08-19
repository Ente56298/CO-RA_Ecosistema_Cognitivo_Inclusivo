# 🎬 Pipeline Automatizado CO•RA

## 🎯 Propósito

Sistema completo de automatización para:
- **Generación de videos** con datos, gráficos y subtítulos
- **Streaming en vivo** con pagos y autenticación por tokens
- **Gestión de eventos** declarativa con YAML

## 🚀 Uso Rápido

### **Generar Video Completo**
```bash
# Comando único para generar video completo
make video SUJETO=sueldos_morelos DATOS=content/sueldos_morelos/data/datos.csv GUION=content/sueldos_morelos/scripts/guion.md

# Configurar proyecto nuevo
make setup PROYECTO=nuevo_tema

# Verificar dependencias
make check
```

### **Streaming en Vivo**
```bash
# Desplegar infraestructura
make deploy

# Crear evento
make event EVENT=2025-08-22-lucha1

# Detener servicios
make stop
```

## 📂 Estructura del Proyecto

```
pipeline_automatizado/
├── scripts/                    # Scripts de procesamiento
│   ├── build_charts.py         # Generador de gráficos
│   ├── md_to_srt.py           # Conversor Markdown → SRT
│   └── render_video.sh        # Renderizador FFmpeg
├── content/                   # Contenido por proyecto
│   └── sueldos_morelos/
│       ├── data/              # CSV con datos
│       ├── scripts/           # Guion en Markdown
│       ├── broll/             # Video de fondo
│       ├── music/             # Música de fondo
│       └── out/               # Archivos generados
├── tenancingo_live/           # Infraestructura streaming
│   ├── web/                   # Aplicación Node.js
│   ├── nginx/                 # Configuración RTMP/HLS
│   ├── events/                # Eventos en YAML
│   └── docker-compose.yml     # Servicios
└── Makefile                   # Automatización
```

## 🎬 Generación de Videos

### **Flujo Automatizado**
1. **Datos** → Gráficos PNG desde CSV
2. **Guion** → Subtítulos SRT desde Markdown  
3. **Edición** → Video vertical 1080x1920 con FFmpeg
4. **Assets** → Título, descripción y miniatura

### **Archivos Requeridos**
- `data/datos.csv` - Datos en formato CSV
- `scripts/guion.md` - Guion en Markdown
- `broll/clip1.mp4` - Video de fondo
- `music/track.mp3` - Música de fondo

### **Salida Generada**
- `out/video_final.mp4` - Video completo
- `out/thumbnail.jpg` - Miniatura
- `out/titulo.txt` - Título para publicación
- `out/descripcion.txt` - Descripción con hashtags

## 📺 Sistema de Streaming

### **Componentes**
- **NGINX RTMP** - Servidor de streaming
- **HLS** - Distribución web
- **Node.js** - Autenticación y pagos
- **PostgreSQL** - Base de datos
- **Redis** - Sesiones

### **Flujo de Evento**
1. **Crear evento** en YAML
2. **Configurar pagos** (Stripe/Conekta)
3. **Iniciar stream** con OBS/FFmpeg
4. **Usuarios compran** acceso
5. **Reciben token** por email
6. **Acceden al stream** con token válido

### **URLs Generadas**
- Landing: `http://localhost:8080/events/evento-id`
- Stream: `http://localhost:8080/watch/evento-id?t=token`
- RTMP: `rtmp://localhost:1935/live/stream_key`
- HLS: `http://localhost:8081/hls/stream_key.m3u8`

## ⚙️ Configuración

### **Variables de Entorno**
```env
# JWT para autenticación
JWT_SECRET=tu_secreto_super_seguro

# Proveedor de pagos
PAYMENT_PROVIDER=stripe

# Base de datos
DB_PASSWORD=password_seguro

# Configuración de streaming
RTMP_URL=rtmp://localhost:1935/live
HLS_URL=http://localhost:8081/hls
```

### **Dependencias**
```bash
# Python
pip install pandas matplotlib

# Sistema
sudo apt install ffmpeg docker docker-compose

# Node.js
cd tenancingo_live/web && npm install
```

## 📋 Ejemplos de Uso

### **Video "Sueldos en Morelos"**
```bash
# 1. Preparar datos
echo "puesto,salario" > content/sueldos_morelos/data/datos.csv
echo "Maestro,25000" >> content/sueldos_morelos/data/datos.csv
echo "Enfermero,30000" >> content/sueldos_morelos/data/datos.csv
echo "Ingeniero,45000" >> content/sueldos_morelos/data/datos.csv

# 2. Crear guion
echo "# Sueldos en Morelos" > content/sueldos_morelos/scripts/guion.md
echo "¿Por qué hay tanta diferencia salarial?" >> content/sueldos_morelos/scripts/guion.md
echo "Analizamos los datos oficiales." >> content/sueldos_morelos/scripts/guion.md

# 3. Generar video
make video SUJETO=sueldos_morelos
```

### **Evento de Streaming**
```yaml
# events/2025-08-22-lucha1.yml
id: lucha1
titulo: "Gran Cartelera Tenancingo"
inicio: "2025-08-22T20:00:00-06:00"
precio_mxn: 79
stream_key: "lucha1_live"
descripcion: "Evento piloto de lucha libre"
```

```bash
# Crear evento y desplegar
make event EVENT=2025-08-22-lucha1
make deploy

# Transmitir con OBS
# RTMP URL: rtmp://localhost:1935/live
# Stream Key: lucha1_live
```

## 🔧 Comandos Disponibles

### **Videos**
- `make video` - Generar video completo
- `make setup PROYECTO=nombre` - Configurar proyecto nuevo
- `make publish-assets` - Generar assets de publicación

### **Streaming**
- `make deploy` - Desplegar infraestructura
- `make event EVENT=nombre` - Crear evento
- `make stop` - Detener servicios

### **Utilidades**
- `make check` - Verificar dependencias
- `make clean` - Limpiar archivos temporales
- `make help` - Mostrar ayuda completa

## 🛡️ Seguridad

### **Autenticación**
- Tokens JWT con expiración
- Stream keys únicos por evento
- Rate limiting en APIs

### **Pagos**
- Webhooks verificados
- Tokens de un solo uso
- Acceso limitado por tiempo

### **Streaming**
- Autenticación RTMP
- CORS configurado
- Logs de acceso

## 📈 Monitoreo

### **Métricas Disponibles**
- Streams activos: `GET /api/streams`
- Estadísticas RTMP: `http://localhost:8081/stat`
- Health check: `http://localhost:8080/health`

### **Logs**
- NGINX: `/var/log/nginx/`
- Aplicación: `docker-compose logs web`
- Base de datos: `docker-compose logs db`

## 🚀 Despliegue en Producción

### **Configuración Mínima**
1. Configurar dominio y SSL
2. Ajustar variables de entorno
3. Configurar proveedor de pagos
4. Configurar SMTP para emails
5. Configurar respaldos de base de datos

### **Escalabilidad**
- Usar CDN para HLS
- Múltiples servidores RTMP
- Load balancer para web
- Redis Cluster para sesiones

---

*Pipeline automatizado para el ecosistema CO•RA* 🎬