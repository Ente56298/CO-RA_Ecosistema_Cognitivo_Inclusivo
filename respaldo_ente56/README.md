# 🛡️ Respaldo Seguro ENTE56 - CO•RA

## 🎯 Propósito

Sistema de respaldo y organización segura de información académica y profesional asociada a la cuenta ENTE56, integrado al ecosistema CO•RA para preservar conocimiento sin comprometer privacidad.

## 📂 Estructura

```
respaldo_ente56/
├── 📄 README.md                 # Este archivo
├── 📁 documentos_publicos/      # Archivos seguros para GitHub
├── 📊 metadatos/               # Índices y listados (sin contenido sensible)
├── 🔧 scripts/                 # Herramientas de extracción y organización
└── 🚫 .gitignore              # Protección de archivos sensibles
```

## 🔐 Principios de Seguridad

### ✅ SÍ se incluye en el repositorio:
- Metadatos (asunto, fecha, nombre de archivo)
- Documentos públicos sin información personal
- Scripts de organización y extracción
- Índices y catálogos de contenido

### ❌ NO se incluye en el repositorio:
- Correos completos con información personal
- Documentos con CURP, RFC, datos bancarios
- Contraseñas, tokens o credenciales
- Archivos de nómina o información financiera
- Datos personales de terceros

## 📋 Categorías de Respaldo

### 📚 Académico (UNADM)
- Trabajos y proyectos académicos
- Recursos educativos
- Comunicaciones institucionales (metadatos)

### 💼 Profesional
- Documentos de trabajo públicos
- Proyectos y desarrollos
- Comunicaciones profesionales (metadatos)

### 🔧 Técnico
- Configuraciones y scripts
- Documentación técnica
- Recursos de desarrollo

## 🚀 Uso

### Generar Metadatos
```bash
python3 scripts/generar_metadatos.py --carpeta "UMED"
python3 scripts/generar_metadatos.py --carpeta "doc importantes"
```

### Organizar Documentos
```bash
python3 scripts/organizar_respaldo.py --categoria "academico"
```

## 🔄 Flujo de Trabajo

1. **Extracción**: Descargar archivos de Outlook/OneDrive a ubicación segura LOCAL
2. **Clasificación**: Separar documentos públicos de privados
3. **Metadatos**: Generar índices sin contenido sensible
4. **Respaldo**: Subir solo metadatos y documentos públicos al repo
5. **Verificación**: Commit con sello verificado

## 🌐 Integración CO•RA

Este módulo se integra con:
- **core_agentes**: Para análisis inteligente de documentos
- **educacion_familiar**: Para recursos educativos
- **accesibilidad**: Para documentos accesibles
- **manifiesto**: Para preservar conocimiento inclusivo

---

*Preservando conocimiento, protegiendo privacidad* 🛡️