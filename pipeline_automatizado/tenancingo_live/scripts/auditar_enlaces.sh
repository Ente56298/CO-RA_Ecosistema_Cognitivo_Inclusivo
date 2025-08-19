#!/bin/bash
# Script de auditoría automática de enlaces
# Genera evidencia técnica para cada URL

set -e

# URLs a auditar
URLS=(
    "https://tenancingolive.byethost17.com/"
    "https://jorgehernandez.22web.org/?i=1"
    "https://coplademun.edomex.gob.mx/index.php/pdm"
    "https://coplademun.edomex.gob.mx/index.php/informe"
    "https://gobernova.com.mx/"
)

# Crear directorio de evidencias
EVIDENCE_DIR="Evidencias_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EVIDENCE_DIR"

echo "🔍 AUDITORÍA AUTOMÁTICA DE ENLACES"
echo "=================================="
echo "Fecha: $(date)"
echo "Directorio: $EVIDENCE_DIR"
echo ""

# Función para auditar una URL
audit_url() {
    local url="$1"
    local index="$2"
    local name="$3"
    
    echo "🌐 Auditando: $url"
    
    # Crear directorio para esta URL
    local url_dir="$EVIDENCE_DIR/${index}_${name}"
    mkdir -p "$url_dir/logs"
    
    # 1. Información básica con curl
    echo "📡 Recolectando información de red..."
    curl -I -L -s -o /dev/null -w "URL: $url\nHTTP Code: %{http_code}\nRedirects: %{num_redirects}\nContent-Type: %{content_type}\nDNS Lookup: %{time_namelookup}s\nConnect: %{time_connect}s\nSSL Handshake: %{time_appconnect}s\nStart Transfer: %{time_starttransfer}s\nTotal Time: %{time_total}s\nSize: %{size_download} bytes\n" "$url" > "$url_dir/logs/curl_info.txt" 2>/dev/null || echo "Error conectando a $url" > "$url_dir/logs/curl_info.txt"
    
    # 2. Headers completos
    echo "📋 Guardando headers..."
    curl -s -D "$url_dir/logs/headers.txt" -o /dev/null "$url" 2>/dev/null || echo "Error obteniendo headers" > "$url_dir/logs/headers.txt"
    
    # 3. Información SSL (solo HTTPS)
    if [[ "$url" == https* ]]; then
        echo "🔒 Verificando certificado SSL..."
        local domain=$(echo "$url" | sed 's|https://||' | sed 's|/.*||' | sed 's|:.*||')
        openssl s_client -servername "$domain" -connect "$domain:443" </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject -dates > "$url_dir/logs/ssl_info.txt" 2>/dev/null || echo "Error verificando SSL" > "$url_dir/logs/ssl_info.txt"
    fi
    
    # 4. Contenido básico para análisis
    echo "📄 Descargando contenido..."
    curl -s -L "$url" | head -100 > "$url_dir/logs/content_sample.txt" 2>/dev/null || echo "Error descargando contenido" > "$url_dir/logs/content_sample.txt"
    
    # 5. Verificar robots.txt y sitemap.xml
    echo "🤖 Verificando robots.txt..."
    local base_url=$(echo "$url" | sed 's|/[^/]*$||')
    curl -s "$base_url/robots.txt" > "$url_dir/logs/robots.txt" 2>/dev/null || echo "robots.txt no encontrado" > "$url_dir/logs/robots.txt"
    
    echo "🗺️ Verificando sitemap.xml..."
    curl -s "$base_url/sitemap.xml" > "$url_dir/logs/sitemap.xml" 2>/dev/null || echo "sitemap.xml no encontrado" > "$url_dir/logs/sitemap.xml"
    
    # 6. Generar reporte de esta URL
    generate_url_report "$url" "$url_dir" "$name"
    
    echo "✅ Auditoría completada para $name"
    echo ""
}

# Función para generar reporte por URL
generate_url_report() {
    local url="$1"
    local dir="$2"
    local name="$3"
    
    local report="$dir/REPORTE_${name}.txt"
    
    cat > "$report" << EOF
REPORTE DE AUDITORÍA - $name
============================
URL: $url
Fecha: $(date)
Auditor: Script Automático

RESULTADOS:
-----------

1. DISPONIBILIDAD:
$(cat "$dir/logs/curl_info.txt" | grep -E "HTTP Code|Total Time|Size")

2. SEGURIDAD SSL:
$(if [[ -f "$dir/logs/ssl_info.txt" ]]; then cat "$dir/logs/ssl_info.txt"; else echo "No aplica (HTTP)"; fi)

3. HEADERS IMPORTANTES:
$(cat "$dir/logs/headers.txt" | grep -i -E "server|content-type|x-frame-options|strict-transport|cache-control" || echo "Headers básicos no encontrados")

4. CONTENIDO:
Título: $(cat "$dir/logs/content_sample.txt" | grep -i "<title>" | head -1 | sed 's/<[^>]*>//g' | xargs || echo "No encontrado")
Meta Description: $(cat "$dir/logs/content_sample.txt" | grep -i "meta.*description" | head -1 || echo "No encontrada")

5. SEO BÁSICO:
Robots.txt: $(if grep -q "User-agent" "$dir/logs/robots.txt" 2>/dev/null; then echo "Presente"; else echo "Ausente"; fi)
Sitemap.xml: $(if grep -q "<urlset\|<url>" "$dir/logs/sitemap.xml" 2>/dev/null; then echo "Presente"; else echo "Ausente"; fi)

6. ESTADO GENERAL:
$(
    http_code=$(cat "$dir/logs/curl_info.txt" | grep "HTTP Code" | cut -d: -f2 | xargs)
    total_time=$(cat "$dir/logs/curl_info.txt" | grep "Total Time" | cut -d: -f2 | sed 's/s//' | xargs)
    
    if [[ "$http_code" == "200" ]]; then
        if (( $(echo "$total_time < 3.0" | bc -l 2>/dev/null || echo 0) )); then
            echo "✅ APROBADO - Sitio funcional y rápido"
        else
            echo "⚠️ OBSERVACIONES - Sitio funcional pero lento ($total_time s)"
        fi
    else
        echo "❌ RECHAZADO - HTTP $http_code"
    fi
)

PRÓXIMOS PASOS:
- Revisar capturas manuales de UI
- Probar funcionalidad en navegador
- Verificar formularios y elementos interactivos
- Confirmar responsive en móvil

EOF
}

# Ejecutar auditoría para cada URL
for i in "${!URLS[@]}"; do
    url="${URLS[$i]}"
    
    # Generar nombre limpio para carpeta
    name=$(echo "$url" | sed 's|https://||' | sed 's|http://||' | sed 's|/.*||' | sed 's|\.|-|g' | sed 's|:|-|g')
    
    audit_url "$url" "$(printf "%02d" $((i+1)))" "$name"
done

# Generar reporte consolidado
echo "📊 Generando reporte consolidado..."
CONSOLIDATED_REPORT="$EVIDENCE_DIR/REPORTE_CONSOLIDADO.txt"

cat > "$CONSOLIDATED_REPORT" << EOF
REPORTE CONSOLIDADO DE AUDITORÍA
================================
Fecha: $(date)
Total URLs auditadas: ${#URLS[@]}

RESUMEN POR URL:
EOF

for i in "${!URLS[@]}"; do
    url="${URLS[$i]}"
    name=$(echo "$url" | sed 's|https://||' | sed 's|http://||' | sed 's|/.*||' | sed 's|\.|-|g' | sed 's|:|-|g')
    dir="$EVIDENCE_DIR/$(printf "%02d" $((i+1)))_${name}"
    
    echo "" >> "$CONSOLIDATED_REPORT"
    echo "$((i+1)). $url" >> "$CONSOLIDATED_REPORT"
    
    if [[ -f "$dir/logs/curl_info.txt" ]]; then
        http_code=$(grep "HTTP Code" "$dir/logs/curl_info.txt" | cut -d: -f2 | xargs)
        total_time=$(grep "Total Time" "$dir/logs/curl_info.txt" | cut -d: -f2 | xargs)
        echo "   Estado: HTTP $http_code" >> "$CONSOLIDATED_REPORT"
        echo "   Tiempo: $total_time" >> "$CONSOLIDATED_REPORT"
        
        if [[ "$http_code" == "200" ]]; then
            echo "   Resultado: ✅ FUNCIONAL" >> "$CONSOLIDATED_REPORT"
        else
            echo "   Resultado: ❌ PROBLEMA" >> "$CONSOLIDATED_REPORT"
        fi
    else
        echo "   Resultado: ❌ ERROR DE CONEXIÓN" >> "$CONSOLIDATED_REPORT"
    fi
done

# Estadísticas finales
functional_count=$(find "$EVIDENCE_DIR" -name "curl_info.txt" -exec grep -l "HTTP Code: 200" {} \; | wc -l)
total_count=${#URLS[@]}

cat >> "$CONSOLIDATED_REPORT" << EOF

ESTADÍSTICAS FINALES:
====================
URLs funcionales: $functional_count/$total_count
Tasa de éxito: $(( functional_count * 100 / total_count ))%

PRÓXIMOS PASOS:
==============
1. Revisar reportes individuales en cada carpeta
2. Realizar pruebas manuales en navegador
3. Capturar screenshots de UI desktop/móvil
4. Probar funcionalidad crítica (formularios, navegación)
5. Completar actas de auditoría por URL

ARCHIVOS GENERADOS:
==================
- Logs técnicos en cada carpeta /logs/
- Reportes individuales por URL
- Este reporte consolidado

EOF

echo "🎉 AUDITORÍA AUTOMÁTICA COMPLETADA"
echo "=================================="
echo "📁 Evidencias guardadas en: $EVIDENCE_DIR"
echo "📊 Reporte consolidado: $CONSOLIDATED_REPORT"
echo ""
echo "📋 RESUMEN:"
echo "   URLs auditadas: $total_count"
echo "   URLs funcionales: $functional_count"
echo "   Tasa de éxito: $(( functional_count * 100 / total_count ))%"
echo ""
echo "🔍 Próximo paso: Revisar reportes y completar auditoría manual"