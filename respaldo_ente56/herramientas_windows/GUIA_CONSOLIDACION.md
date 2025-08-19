# 🏗️ Guía de Consolidación de Monorepo - CO•RA

## 🎯 Propósito

Transforma proyectos dispersos y desorganizados en una estructura monorepo limpia y modular, facilitando el mantenimiento y desarrollo.

## 📂 Estructura Objetivo

```
proyecto-consolidado/
├── apps/                    # Aplicaciones principales
│   ├── backend-php/         # API y lógica PHP
│   ├── backend-node/        # Servicios Node.js/TypeScript
│   └── frontend/            # Interfaces React/Vue/Angular
├── workers/                 # Procesos en segundo plano
│   └── python/              # Scripts Python, APIs, crons
├── infra/                   # Infraestructura y servicios
│   ├── nginx/               # Configuración Nginx/RTMP
│   ├── ffmpeg/              # Herramientas de video
│   └── database/            # Esquemas SQL, migraciones
├── modules/                 # Módulos reutilizables
│   ├── streaming/           # Lógica de streaming
│   └── webrtc/              # VideoWhisper, WebRTC
├── public/                  # Assets públicos
│   ├── css/                 # Estilos
│   ├── js/                  # JavaScript frontend
│   ├── img/                 # Imágenes
│   └── admin/               # Panel administrativo
├── docs/                    # Documentación
├── config/                  # Configuración centralizada
├── legacy/                  # Código heredado
└── tools/                   # Herramientas de desarrollo
```

## 🚀 Uso del Consolidador

### **Opción 1: Ejecución Rápida**
```batch
# Doble clic en:
EJECUTAR_CONSOLIDACION.bat
```

### **Opción 2: PowerShell Manual**
```powershell
# Simulación (recomendado primero)
.\Consolidar-Monorepo.ps1 -Root "A:\wamp64\www\mi_proyecto" -DryRun

# Copiar archivos (mantiene originales)
.\Consolidar-Monorepo.ps1 -Root "A:\wamp64\www\mi_proyecto"

# Mover archivos (reorganiza completamente)
.\Consolidar-Monorepo.ps1 -Root "A:\wamp64\www\mi_proyecto" -Move
```

## 📋 Proceso de Consolidación

### **1. Análisis Inicial**
- Escanea toda la estructura del proyecto
- Identifica tipos de archivos y carpetas
- Planifica la migración según patrones

### **2. Creación de Estructura**
- Crea carpetas del monorepo
- Organiza por función y tecnología
- Mantiene separación de responsabilidades

### **3. Migración Inteligente**
- **PHP**: `apps/backend-php/`
- **Node.js**: `apps/backend-node/`
- **Python**: `workers/python/`
- **Frontend**: `apps/frontend/`
- **Assets**: `public/`
- **Docs**: `docs/`
- **Config**: `config/`

### **4. Consolidación de Configuración**
- Unifica archivos `.env*`
- Crea `.env.sample` con plantilla
- Centraliza configuración

### **5. Generación de Reportes**
- `migration_report.json` - Detalles completos
- `README.md` - Documentación del monorepo
- `.gitignore` - Exclusiones estándar

## 🔧 Reglas de Migración

### **Backend PHP**
```
Archivos: *.php, index.php, login.php, admin*.php, api.php
Destino: apps/backend-php/
```

### **Backend Node.js**
```
Archivos: package.json, *.js, *.ts, *_api.js, *_cron.js
Destino: apps/backend-node/
```

### **Workers Python**
```
Archivos: *.py, requirements.txt, voucher_*.py
Destino: workers/python/
```

### **Base de Datos**
```
Archivos: *.sql, setup_database.php, migrate_*.php
Destino: infra/database/
```

### **Assets Públicos**
```
Carpetas: css/, js/, img/, admin/, live/
Archivos: *.html, .htaccess*
Destino: public/
```

### **Configuración**
```
Archivos: config*.php, .env*, session_config.php
Destino: config/
```

### **Infraestructura**
```
Carpetas: nginx-rtmp/, ffmpeg/, FFmpeg-master/
Destino: infra/nginx/, infra/ffmpeg/
```

### **Módulos Streaming**
```
Carpetas: videowhisper*, streaming*
Destino: modules/webrtc/, modules/streaming/
```

### **Legacy**
```
Carpetas: MonaServer_Win64/, red5-flex-streamer/, GoldenX-CASINO-SITE/
Destino: legacy/
```

## 📊 Ejemplo de Reporte

### **migration_report.json**
```json
{
  "timestamp": "2024-01-15 14:30:22",
  "mode": "copy",
  "total_items": 127,
  "successful": 125,
  "failed": 2,
  "structure_created": [
    "apps/backend-php",
    "apps/backend-node",
    "workers/python",
    "public",
    "docs"
  ],
  "items": [
    {
      "action": "copy",
      "source": "A:\\proyecto\\index.php",
      "dest": "A:\\proyecto\\apps\\backend-php\\index.php",
      "status": "success"
    }
  ]
}
```

## ✅ Beneficios del Monorepo

### **Organización**
- Estructura clara y predecible
- Separación por responsabilidades
- Fácil navegación y mantenimiento

### **Desarrollo**
- Configuración centralizada
- Dependencias compartidas
- Herramientas unificadas

### **Despliegue**
- Build scripts centralizados
- CI/CD simplificado
- Versionado coherente

### **Colaboración**
- Código compartido visible
- Estándares unificados
- Documentación centralizada

## 🛡️ Seguridad y Respaldos

### **Antes de Ejecutar**
- ✅ Crear respaldo completo del proyecto
- ✅ Verificar permisos de escritura
- ✅ Ejecutar simulación primero (`-DryRun`)

### **Durante la Ejecución**
- ✅ Monitorear mensajes de error
- ✅ Verificar espacio en disco
- ✅ Revisar archivos críticos

### **Después de la Consolidación**
- ✅ Verificar estructura creada
- ✅ Probar funcionalidad básica
- ✅ Revisar `migration_report.json`
- ✅ Actualizar documentación

## 🔧 Solución de Problemas

### **Error: Permisos Insuficientes**
```powershell
# Ejecutar PowerShell como Administrador
```

### **Error: Archivos en Uso**
```powershell
# Cerrar aplicaciones que usen los archivos
# Detener servicios web (Apache, IIS)
```

### **Error: Espacio Insuficiente**
```powershell
# Verificar espacio en disco
# Usar -Move en lugar de copiar
```

### **Reversión de Cambios**
```powershell
# Si usaste -Move, restaurar desde respaldo
# Si copiaste, eliminar carpetas nuevas
```

## 📈 Próximos Pasos

### **Después de la Consolidación**
1. **Configurar entorno**:
   ```bash
   cp config/.env.sample config/.env
   # Editar config/.env
   ```

2. **Instalar dependencias**:
   ```bash
   cd apps/backend-node && npm install
   cd workers/python && pip install -r requirements.txt
   ```

3. **Configurar servidor web**:
   - Apuntar DocumentRoot a `public/`
   - Configurar rutas de API
   - Ajustar permisos

4. **Probar funcionalidad**:
   - Verificar páginas principales
   - Probar APIs
   - Validar base de datos

---

*Herramienta de consolidación para el ecosistema CO•RA* 🏗️