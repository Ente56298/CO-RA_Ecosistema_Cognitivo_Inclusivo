#!/bin/bash
echo "🔍 Verificando ritual CO•RA..."
for i in {1..10}; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://ente56298.github.io/CO-RA_Ecosistema_Cognitivo_Inclusivo/)
  if [ "$status" = "200" ]; then
    echo "✅ RITUAL ACTIVO: https://ente56298.github.io/CO-RA_Ecosistema_Cognitivo_Inclusivo/"
    exit 0
  fi
  echo "⏳ Intento $i/10 - Status: $status"
  sleep 30
done
echo "❌ Ritual aún no activo. Verificar configuración GitHub Pages."
