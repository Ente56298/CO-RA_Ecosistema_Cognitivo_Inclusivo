# 📋 Paquete de Evidencia de Enlaces - Lanzamiento TenancingoLive

## 🎯 Alcance y Entregables

### **Enlaces a Auditar**:
1. `https://tenancingolive.byethost17.com/`
2. `https://jorgehernandez.22web.org/?i=1`
3. `https://coplademun.edomex.gob.mx/index.php/pdm`
4. `https://coplademun.edomex.gob.mx/index.php/informe`
5. `https://reportes.edomex.gob.mx:8443/pentaho/api/repos/%3Ahome%3Acoplademun%3ALineas_atendidas_x_pilar_anio.prpt/viewer?mun=107&ayuntamiento=107`
6. `https://gobernova.com.mx/`

### **Entregables por Enlace**:
- ✅ **Evidencia PDF** con capturas y resultados
- ✅ **Acta de auditoría** firmada
- ✅ **Carpeta fuente** con capturas PNG + logs TXT

---

## 🔍 Evidencia a Recolectar por Enlace

### **1. Disponibilidad y Red**
- HTTP status final, redirecciones, TTFB, tiempo total
- Resolución DNS y dirección IP

### **2. Seguridad**
- Certificado SSL vigente (emisor, sujeto, fechas)
- Sin contenido mixto ni advertencias

### **3. Contenido y Metadatos**
- Título H1 visible, `<title>` y meta description
- Open Graph/Twitter Card
- Favicon cargando

### **4. Funcionalidad**
- Navegación principal, enlaces internos/externos
- Formularios (envío/recepción), reproductores embebidos

### **5. Consola/Recursos**
- Captura consola sin errores
- Recursos bloqueados/CORS ausentes

### **6. Rendimiento**
- Peso total home, número de requests
- Carga móvil en 4G

### **7. SEO Básico**
- robots.txt, sitemap.xml, H1 único

### **8. Legal/Transparencia**
- Aviso privacidad, términos, contacto visible

---

## 🧪 Procedimiento de Prueba por Enlace

### **Paso 1: UI Desktop/Móvil**
```bash
# Etiqueta: Evidencia UI
# Captura pantalla completa (desktop y móvil)
```

### **Paso 2: Inspeccionar Seguridad**
```bash
# Etiqueta: SSL
# Ver candado → Certificado → Captura emisor, sujeto, validez
```

### **Paso 3: Medir Red**
```bash
# Etiqueta: Red
# Network tab → reload → capturar:
# - Primer request: Status, TTFB, Content-Type
# - Resumen: requests y peso total
```

### **Paso 4: Consola**
```bash
# Etiqueta: Consola
# Captura sin errores (o lista errores si aparecen)
```

### **Paso 5: Metadatos**
```bash
# Etiqueta: Metas
# Ver código fuente → capturar <title>, description, OG
```

### **Paso 6: Funcionalidad Crítica**
```bash
# Etiqueta: Flujo
# Navegar menú, enviar formulario, reproducir video
# Capturar confirmaciones/éxito
```

### **Paso 7: Archivos Auxiliares**
```bash
# Etiqueta: Robots/Sitemap
# Abrir /robots.txt y /sitemap.xml → capturas
```

### **Paso 8: Prueba 404**
```bash
# Etiqueta: Error 404
# Visitar /no-existe → capturar página error personalizada
```

---

## 📄 Plantilla de Acta de Auditoría

| Campo | Detalle |
|-------|---------|
| **Enlace** | |
| **Fecha y hora local** | |
| **Auditor** | |
| **Estado general** | Aprobado / Observaciones / Rechazado |
| **Disponibilidad** | HTTP status final, redirecciones |
| **Desempeño** | TTFB, tiempo total, requests, peso |
| **Seguridad** | Emisor SSL, válido hasta, HSTS/mixto |
| **Consola** | Errores/Warnings relevantes |
| **SEO básico** | Title, Description, H1, OG/Twitter |
| **Funcionalidad** | Navegación, formularios, embeds |
| **Robots/Sitemap** | Accesibles y correctos |
| **Incidencias** | Lista con pasos para reproducir |
| **Acciones correctivas** | Dueño, fecha objetivo |
| **Decisión** | Aprobado para lanzamiento: Sí/No |
| **Firma** | |

---

## 📁 Estructura de Carpetas

```
Evidencias/
├── 01_TenancingoLive/
│   ├── 2025-08-19_Acta.pdf
│   ├── capturas/
│   │   ├── UI_desktop.png
│   │   ├── UI_mobile.png
│   │   ├── SSL.png
│   │   ├── Network.png
│   │   ├── Console.png
│   │   ├── Metas.png
│   │   ├── Flujo_formulario.png
│   │   ├── Robots.png
│   │   └── 404.png
│   └── logs/
│       ├── curl.txt
│       ├── headers.txt
│       └── ssl_info.txt
├── 02_JorgeHernandez/
├── 03_COPLADEMUN_PDM/
├── 04_COPLADEMUN_Informe/
├── 05_Pentaho_LineasPorPilar/
└── 06_Gobernova/
```

---

## 🔧 Comandos de Evidencia Técnica

### **Encabezados y Tiempos con curl**
```bash
curl -I -L -s -o /dev/null -w "http_code:%{http_code}\nredirects:%{num_redirects}\ncontent_type:%{content_type}\nnamelookup:%{time_namelookup}\nconnect:%{time_connect}\nappconnect:%{time_appconnect}\nstarttransfer:%{time_starttransfer}\ntotal:%{time_total}\n" https://tenancingolive.byethost17.com/
```

### **Detalles de Certificado**
```bash
openssl s_client -servername tenancingolive.byethost17.com -connect tenancingolive.byethost17.com:443 </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject -dates
```

### **Guardar Headers Completos**
```bash
curl -s -D headers.txt -o /dev/null https://tenancingolive.byethost17.com/
```

---

## 🎯 Pautas Específicas por Enlace

### **TenancingoLive**
- **Pruebas clave**: Portada, navegación, reproductor/stream, formulario contacto
- **Especial**: Prueba desde 4G y Wi-Fi, confirmar sin contenido mixto

### **JorgeHernandez**
- **Pruebas clave**: Menú, formulario contacto, coherencia identidad visual

### **COPLADEMUN PDM/Informe**
- **Pruebas clave**: Accesibilidad, carga < 5s, enlaces documentos
- **Evidencia**: Capturas secciones relevantes como referencia metodológica

### **Pentaho (Líneas por Pilar)**
- **Pruebas clave**: Carga reporte con filtros, botones exportación, gráficos visibles
- **Seguridad**: Enmascarar datos sensibles en capturas

### **Gobernova**
- **Pruebas clave**: Secciones servicios/metodologías, tiempos carga, enlaces contacto

---

## ✅ Criterio de "Aprobado al 100%"

**Solo se marca CERTIFICADO si**:
- ✅ Contenido publicado es última versión
- ✅ Todas las rutas internas funcionan
- ✅ Sin errores críticos en consola
- ✅ Diseño responsive móvil/desktop
- ✅ Formularios/elementos interactivos operativos
- ✅ HTTPS operativo sin advertencias

---

## 🔒 Cierre y Certificación

### **Compilación Final**:
1. ✅ Cada carpeta evidencia en PDF con acta
2. ✅ Firma electrónica en acta o rúbrica escaneada
3. ✅ Archivos fuente conservados para trazabilidad
4. ✅ **Checklist final**: Todos enlaces "Aprobado" sin incidencias

### **Declaración de Certificación**:
```
🔒 TODOS LOS ENLACES CERTIFICADOS AL 100%
📋 EVIDENCIA COMPLETA DOCUMENTADA
🚀 TENANCINGLIVE LISTO PARA LANZAMIENTO PÚBLICO
```

---

*Paquete completo de evidencia para lanzamiento sin errores* 📋