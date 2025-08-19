#!/bin/bash
# Script de certificación completa automatizada
# Ejecuta todas las validaciones y genera reporte final

set -e

DOMAIN="tenancingo.byethost17.com"
BASE_URL="https://$DOMAIN"
REPORT_FILE="certificacion_$(date +%Y%m%d_%H%M%S).txt"

echo "🔒 CERTIFICACIÓN INTEGRAL TENANCINGLIVE" | tee $REPORT_FILE
echo "=======================================" | tee -a $REPORT_FILE
echo "Fecha: $(date)" | tee -a $REPORT_FILE
echo "Dominio: $DOMAIN" | tee -a $REPORT_FILE
echo "" | tee -a $REPORT_FILE

# Contadores
TOTAL_TESTS=0
PASSED_TESTS=0
CRITICAL_TESTS=0
CRITICAL_PASSED=0

function test_critical() {
    local name="$1"
    local command="$2"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    CRITICAL_TESTS=$((CRITICAL_TESTS + 1))
    
    echo -n "🔍 $name... " | tee -a $REPORT_FILE
    
    if eval "$command" &>/dev/null; then
        echo "✅ PASS" | tee -a $REPORT_FILE
        PASSED_TESTS=$((PASSED_TESTS + 1))
        CRITICAL_PASSED=$((CRITICAL_PASSED + 1))
        return 0
    else
        echo "❌ FAIL" | tee -a $REPORT_FILE
        return 1
    fi
}

function test_normal() {
    local name="$1"
    local command="$2"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "🔍 $name... " | tee -a $REPORT_FILE
    
    if eval "$command" &>/dev/null; then
        echo "✅ PASS" | tee -a $REPORT_FILE
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo "⚠️  WARN" | tee -a $REPORT_FILE
        return 1
    fi
}

# ETAPA 1: CERTIFICACIÓN TÉCNICA
echo "📋 ETAPA 1: CERTIFICACIÓN TÉCNICA" | tee -a $REPORT_FILE
echo "=================================" | tee -a $REPORT_FILE

test_critical "SSL Válido" "curl -s -I $BASE_URL | grep -q 'HTTP/2 200\|HTTP/1.1 200'"
test_critical "Redirección HTTPS" "curl -s -I http://$DOMAIN | grep -q 'Location.*https'"
test_critical "Tiempo de carga < 3s" "[[ \$(curl -w '%{time_total}' -s -o /dev/null $BASE_URL | cut -d. -f1) -lt 3 ]]"
test_critical "Página principal carga" "curl -s $BASE_URL | grep -q -i 'tenancingo'"

# ETAPA 2: CERTIFICACIÓN DE SEGURIDAD
echo "" | tee -a $REPORT_FILE
echo "🛡️ ETAPA 2: CERTIFICACIÓN DE SEGURIDAD" | tee -a $REPORT_FILE
echo "======================================" | tee -a $REPORT_FILE

test_critical "Headers de seguridad" "curl -s -I $BASE_URL | grep -q 'X-Frame-Options\|X-Content-Type-Options'"
test_critical "Config.php no público" "! curl -s $BASE_URL/config.php | grep -q '<?php'"
test_normal "Compresión GZIP" "curl -s -H 'Accept-Encoding: gzip' -I $BASE_URL | grep -q 'Content-Encoding: gzip'"

# ETAPA 3: CERTIFICACIÓN DE CONTENIDO
echo "" | tee -a $REPORT_FILE
echo "🗂️ ETAPA 3: CERTIFICACIÓN DE CONTENIDO" | tee -a $REPORT_FILE
echo "======================================" | tee -a $REPORT_FILE

test_critical "Sin contenido placeholder" "! curl -s $BASE_URL | grep -q -i 'lorem ipsum\|placeholder'"
test_critical "Título personalizado" "curl -s $BASE_URL | grep -q '<title>.*TenancingoLive'"
test_normal "Favicon presente" "curl -s -I $BASE_URL/favicon.ico | grep -q '200'"

# ETAPA 4: CERTIFICACIÓN SEO
echo "" | tee -a $REPORT_FILE
echo "🔍 ETAPA 4: CERTIFICACIÓN SEO" | tee -a $REPORT_FILE
echo "=============================" | tee -a $REPORT_FILE

test_normal "Sitemap accesible" "curl -s $BASE_URL/sitemap.xml | grep -q '<urlset\|<url>'"
test_normal "Robots.txt presente" "curl -s $BASE_URL/robots.txt | grep -q 'User-agent'"
test_normal "Meta description" "curl -s $BASE_URL | grep -q '<meta name=\"description\"'"

# ETAPA 5: CERTIFICACIÓN FUNCIONAL
echo "" | tee -a $REPORT_FILE
echo "⚙️ ETAPA 5: CERTIFICACIÓN FUNCIONAL" | tee -a $REPORT_FILE
echo "===================================" | tee -a $REPORT_FILE

test_critical "Página 404 personalizada" "curl -s $BASE_URL/no-existe | grep -q -i 'tenancingo\|404'"
test_critical "Webhook pagos responde" "curl -s -X POST $BASE_URL/webhook_pago.php -H 'Content-Type: application/json' -d '{}' | grep -q 'error\|invalid'"

# RESUMEN FINAL
echo "" | tee -a $REPORT_FILE
echo "📊 RESUMEN DE CERTIFICACIÓN" | tee -a $REPORT_FILE
echo "===========================" | tee -a $REPORT_FILE
echo "Total de pruebas: $TOTAL_TESTS" | tee -a $REPORT_FILE
echo "Pruebas pasadas: $PASSED_TESTS" | tee -a $REPORT_FILE
echo "Pruebas críticas: $CRITICAL_TESTS" | tee -a $REPORT_FILE
echo "Críticas pasadas: $CRITICAL_PASSED" | tee -a $REPORT_FILE

SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
CRITICAL_RATE=$((CRITICAL_PASSED * 100 / CRITICAL_TESTS))

echo "Tasa de éxito: $SUCCESS_RATE%" | tee -a $REPORT_FILE
echo "Críticas completadas: $CRITICAL_RATE%" | tee -a $REPORT_FILE

# VEREDICTO FINAL
echo "" | tee -a $REPORT_FILE
echo "🎯 VEREDICTO FINAL" | tee -a $REPORT_FILE
echo "==================" | tee -a $REPORT_FILE

if [ $CRITICAL_RATE -eq 100 ] && [ $SUCCESS_RATE -ge 80 ]; then
    echo "✅ CERTIFICADO AL 100%" | tee -a $REPORT_FILE
    echo "🚀 TenancingoLive LISTO PARA LANZAMIENTO PÚBLICO" | tee -a $REPORT_FILE
    CERTIFIED=true
elif [ $CRITICAL_RATE -ge 80 ] && [ $SUCCESS_RATE -ge 70 ]; then
    echo "⚠️  CASI CERTIFICADO" | tee -a $REPORT_FILE
    echo "🔧 Corregir elementos críticos pendientes" | tee -a $REPORT_FILE
    CERTIFIED=false
else
    echo "❌ NO CERTIFICADO" | tee -a $REPORT_FILE
    echo "🚫 Requiere trabajo adicional antes del lanzamiento" | tee -a $REPORT_FILE
    CERTIFIED=false
fi

# PRÓXIMOS PASOS
echo "" | tee -a $REPORT_FILE
echo "📋 PRÓXIMOS PASOS" | tee -a $REPORT_FILE
echo "=================" | tee -a $REPORT_FILE

if [ "$CERTIFIED" = true ]; then
    echo "1. ✅ Generar Acta de Certificación oficial" | tee -a $REPORT_FILE
    echo "2. ✅ Configurar monitoreo de uptime" | tee -a $REPORT_FILE
    echo "3. ✅ Preparar anuncio de lanzamiento" | tee -a $REPORT_FILE
    echo "4. ✅ Activar analytics y seguimiento" | tee -a $REPORT_FILE
else
    echo "1. 🔧 Corregir pruebas fallidas críticas" | tee -a $REPORT_FILE
    echo "2. 🔧 Revisar elementos de seguridad" | tee -a $REPORT_FILE
    echo "3. 🔧 Completar contenido faltante" | tee -a $REPORT_FILE
    echo "4. 🔧 Re-ejecutar certificación" | tee -a $REPORT_FILE
fi

echo "" | tee -a $REPORT_FILE
echo "📄 Reporte guardado en: $REPORT_FILE" | tee -a $REPORT_FILE
echo "🕒 Certificación completada: $(date)" | tee -a $REPORT_FILE

# Mostrar resultado final
if [ "$CERTIFIED" = true ]; then
    echo ""
    echo "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
    echo "🎉  TENANCINGLIVE CERTIFICADO AL 100%  🎉"
    echo "🎉     LISTO PARA LANZAMIENTO PÚBLICO    🎉"
    echo "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
    exit 0
else
    echo ""
    echo "⚠️  CERTIFICACIÓN INCOMPLETA"
    echo "🔧 Revisar elementos pendientes antes del lanzamiento"
    exit 1
fi