#!/bin/bash
# Script de validación automática para TenancingoLive
# Verifica criterios críticos de producción

set -e

DOMAIN="tenancingo.byethost17.com"
BASE_URL="https://$DOMAIN"
TEMP_DIR="/tmp/tenancingo_validation"

echo "🔍 Validando TenancingoLive para producción..."
echo "🌐 Dominio: $DOMAIN"
echo "📅 Fecha: $(date)"

# Crear directorio temporal
mkdir -p $TEMP_DIR
cd $TEMP_DIR

# Contadores
PASSED=0
FAILED=0
WARNINGS=0

function test_result() {
    local test_name="$1"
    local result="$2"
    local message="$3"
    
    if [ "$result" = "PASS" ]; then
        echo "✅ $test_name: $message"
        ((PASSED++))
    elif [ "$result" = "WARN" ]; then
        echo "⚠️  $test_name: $message"
        ((WARNINGS++))
    else
        echo "❌ $test_name: $message"
        ((FAILED++))
    fi
}

# BLOQUE 1: HTTPS y Dominio
echo -e "\n🔒 BLOQUE 1: HTTPS y Dominio"

# Test HTTPS
if curl -s -I "$BASE_URL" | grep -q "HTTP/2 200\|HTTP/1.1 200"; then
    test_result "HTTPS" "PASS" "Sitio responde correctamente"
else
    test_result "HTTPS" "FAIL" "Sitio no responde o error HTTP"
fi

# Test redirección HTTP->HTTPS
HTTP_REDIRECT=$(curl -s -I "http://$DOMAIN" | grep -i location | grep https || echo "")
if [ -n "$HTTP_REDIRECT" ]; then
    test_result "HTTP Redirect" "PASS" "Redirección HTTP->HTTPS activa"
else
    test_result "HTTP Redirect" "WARN" "Redirección HTTP->HTTPS no detectada"
fi

# Test certificado SSL
if openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" </dev/null 2>/dev/null | grep -q "Verify return code: 0"; then
    test_result "SSL Certificate" "PASS" "Certificado SSL válido"
else
    test_result "SSL Certificate" "FAIL" "Certificado SSL inválido o expirado"
fi

# BLOQUE 2: Navegación y Enlaces
echo -e "\n🧭 BLOQUE 2: Navegación y Enlaces"

# Test páginas principales
PAGES=("/" "/eventos" "/contacto" "/dashboard.html")
for page in "${PAGES[@]}"; do
    if curl -s -I "$BASE_URL$page" | grep -q "200"; then
        test_result "Página $page" "PASS" "Carga correctamente"
    else
        test_result "Página $page" "FAIL" "No carga o error HTTP"
    fi
done

# Test 404 personalizada
if curl -s "$BASE_URL/no-existe-esta-pagina" | grep -q -i "tenancingo\|404\|no encontrada"; then
    test_result "Página 404" "PASS" "Página 404 personalizada"
else
    test_result "Página 404" "WARN" "Página 404 genérica o no personalizada"
fi

# BLOQUE 3: SEO Básico
echo -e "\n🔍 BLOQUE 3: SEO Básico"

# Test sitemap
if curl -s "$BASE_URL/sitemap.xml" | grep -q "<urlset\|<url>"; then
    test_result "Sitemap" "PASS" "Sitemap.xml accesible"
else
    test_result "Sitemap" "FAIL" "Sitemap.xml no encontrado"
fi

# Test robots.txt
if curl -s "$BASE_URL/robots.txt" | grep -q "User-agent\|Sitemap"; then
    test_result "Robots.txt" "PASS" "Robots.txt configurado"
else
    test_result "Robots.txt" "WARN" "Robots.txt no encontrado o vacío"
fi

# Test meta tags en homepage
HOME_CONTENT=$(curl -s "$BASE_URL/")
if echo "$HOME_CONTENT" | grep -q "<title>.*TenancingoLive"; then
    test_result "Title Tag" "PASS" "Título personalizado encontrado"
else
    test_result "Title Tag" "FAIL" "Título genérico o faltante"
fi

if echo "$HOME_CONTENT" | grep -q '<meta name="description"'; then
    test_result "Meta Description" "PASS" "Meta descripción presente"
else
    test_result "Meta Description" "WARN" "Meta descripción faltante"
fi

# BLOQUE 4: Funcionalidad Crítica
echo -e "\n⚙️ BLOQUE 4: Funcionalidad Crítica"

# Test base de datos (indirecto - verificar si config.php existe)
if curl -s "$BASE_URL/config.php" | grep -q "<?php\|function\|define"; then
    test_result "Config PHP" "WARN" "Config.php accesible públicamente - RIESGO DE SEGURIDAD"
else
    test_result "Config PHP" "PASS" "Config.php no accesible públicamente"
fi

# Test webhook de pagos
if curl -s -X POST "$BASE_URL/webhook_pago.php" -H "Content-Type: application/json" -d '{}' | grep -q "error\|invalid\|missing"; then
    test_result "Webhook Pagos" "PASS" "Webhook responde a requests"
else
    test_result "Webhook Pagos" "WARN" "Webhook no responde o error"
fi

# BLOQUE 5: Rendimiento Básico
echo -e "\n⚡ BLOQUE 5: Rendimiento"

# Test tiempo de carga
LOAD_TIME=$(curl -w "%{time_total}" -s -o /dev/null "$BASE_URL/")
if (( $(echo "$LOAD_TIME < 3.0" | bc -l) )); then
    test_result "Tiempo de Carga" "PASS" "Carga en ${LOAD_TIME}s (< 3s)"
elif (( $(echo "$LOAD_TIME < 5.0" | bc -l) )); then
    test_result "Tiempo de Carga" "WARN" "Carga en ${LOAD_TIME}s (3-5s)"
else
    test_result "Tiempo de Carga" "FAIL" "Carga en ${LOAD_TIME}s (> 5s)"
fi

# Test compresión
if curl -s -H "Accept-Encoding: gzip" -I "$BASE_URL/" | grep -q "Content-Encoding: gzip"; then
    test_result "Compresión GZIP" "PASS" "Compresión activa"
else
    test_result "Compresión GZIP" "WARN" "Compresión no detectada"
fi

# BLOQUE 6: Seguridad Básica
echo -e "\n🛡️ BLOQUE 6: Seguridad"

# Test headers de seguridad
HEADERS=$(curl -s -I "$BASE_URL/")
if echo "$HEADERS" | grep -q "X-Frame-Options\|X-Content-Type-Options"; then
    test_result "Security Headers" "PASS" "Headers de seguridad presentes"
else
    test_result "Security Headers" "WARN" "Headers de seguridad faltantes"
fi

# Test directorio admin
if curl -s -I "$BASE_URL/admin" | grep -q "401\|403\|404"; then
    test_result "Admin Protection" "PASS" "Directorio admin protegido"
else
    test_result "Admin Protection" "WARN" "Directorio admin accesible"
fi

# BLOQUE 7: Contenido
echo -e "\n📝 BLOQUE 7: Contenido"

# Test contenido placeholder
if echo "$HOME_CONTENT" | grep -q -i "lorem ipsum\|placeholder\|ejemplo\|test"; then
    test_result "Contenido Real" "WARN" "Contenido placeholder detectado"
else
    test_result "Contenido Real" "PASS" "Contenido real presente"
fi

# Test favicon
if curl -s -I "$BASE_URL/favicon.ico" | grep -q "200"; then
    test_result "Favicon" "PASS" "Favicon presente"
else
    test_result "Favicon" "WARN" "Favicon faltante"
fi

# RESUMEN FINAL
echo -e "\n" + "="*60
echo "📊 RESUMEN DE VALIDACIÓN"
echo "="*60
echo "✅ Pruebas pasadas: $PASSED"
echo "⚠️  Advertencias: $WARNINGS"
echo "❌ Pruebas fallidas: $FAILED"

TOTAL=$((PASSED + WARNINGS + FAILED))
SUCCESS_RATE=$((PASSED * 100 / TOTAL))

echo "📈 Tasa de éxito: $SUCCESS_RATE%"

# Determinar estado general
if [ $FAILED -eq 0 ] && [ $SUCCESS_RATE -ge 80 ]; then
    echo -e "\n🎉 ESTADO: LISTO PARA PRODUCCIÓN"
    echo "✅ TenancingoLive cumple criterios mínimos"
elif [ $FAILED -le 2 ] && [ $SUCCESS_RATE -ge 70 ]; then
    echo -e "\n⚠️  ESTADO: CASI LISTO"
    echo "🔧 Corregir errores críticos antes de lanzar"
else
    echo -e "\n❌ ESTADO: NO LISTO"
    echo "🚫 Requiere trabajo adicional antes de producción"
fi

# Recomendaciones
echo -e "\n💡 PRÓXIMOS PASOS:"
if [ $FAILED -gt 0 ]; then
    echo "1. Corregir errores críticos (❌)"
fi
if [ $WARNINGS -gt 3 ]; then
    echo "2. Revisar advertencias importantes (⚠️)"
fi
echo "3. Ejecutar validación manual con CHECKLIST_100_PRODUCCION.md"
echo "4. Probar en dispositivos móviles reales"
echo "5. Configurar monitoreo de uptime"

# Limpiar archivos temporales
cd /
rm -rf $TEMP_DIR

echo -e "\n🔍 Validación completada - $(date)"

# Exit code basado en resultados
if [ $FAILED -eq 0 ]; then
    exit 0
else
    exit 1
fi