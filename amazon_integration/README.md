# 🛒 Amazon Integration - CO•RA

## 🎯 Propósito

Sistema automatizado para generar enlaces de afiliado de Amazon a partir de contenido en templates, integrado con GitHub Actions para ejecución automática.

## 📂 Estructura

```
amazon_integration/
├── scripts/
│   └── generar_enlaces.py     # Generador principal
├── templates/                 # Templates con productos
│   └── ejemplo_producto.md    # Ejemplo de uso
├── data/
│   ├── links.csv             # Enlaces generados (auto)
│   └── reporte_enlaces.json  # Reporte detallado (auto)
└── README.md                 # Esta documentación
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Tag de afiliado de Amazon (requerido)
AMAZON_AFFILIATE_TAG=tu-tag-20
```

### GitHub Secrets

En tu repositorio, configura:
- `AMAZON_AFFILIATE_TAG`: Tu tag de afiliado de Amazon

## 🚀 Uso

### Manual

```bash
# Ejecutar generación de enlaces
python amazon_integration/scripts/generar_enlaces.py
```

### Automático

El sistema se ejecuta automáticamente cuando:
- Se modifica cualquier archivo en `templates/`
- Se hace push o pull request
- Se ejecuta manualmente desde GitHub Actions

## 📝 Formato de Templates

### ASINs Directos
```markdown
Producto recomendado: B08N5WRWNW
```

### URLs de Amazon
```markdown
[Producto](https://www.amazon.com/dp/B07FNJB8TT)
```

## 📊 Salida

### CSV (`data/links.csv`)
```csv
asin,enlace_afiliado,archivo_origen,tipo,fecha_generacion,tag_afiliado
B08N5WRWNW,https://www.amazon.com/dp/B08N5WRWNW?tag=cora-20,templates/ejemplo.md,asin_directo,2024-01-15T10:30:00,cora-20
```

### JSON (`data/reporte_enlaces.json`)
```json
{
  "fecha_generacion": "2024-01-15T10:30:00",
  "total_enlaces": 5,
  "tag_afiliado": "cora-20",
  "enlaces": [...],
  "estadisticas": {
    "por_tipo": {"asin_directo": 3, "url_amazon": 2},
    "por_archivo": {"templates/ejemplo.md": 5}
  }
}
```

## 🔄 Flujo de Trabajo

1. **Detección**: GitHub Actions detecta cambios en `templates/`
2. **Extracción**: Script escanea archivos buscando ASINs y URLs
3. **Generación**: Crea enlaces de afiliado con tu tag
4. **Guardado**: Actualiza `data/links.csv` y reporte JSON
5. **Commit**: Sube cambios automáticamente al repo

## 🛡️ Seguridad

- Tag de afiliado se almacena como secret
- Solo se procesan archivos en `templates/`
- Commits automáticos usan email noreply verificado

## 🌐 Integración CO•RA

Este módulo se integra con:
- **core_agentes**: Para recomendaciones inteligentes
- **accesibilidad**: Para productos inclusivos
- **educacion_familiar**: Para recursos educativos

---

*Monetización ética para sostener el ecosistema CO•RA* 💰