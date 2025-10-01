#!/bin/bash
echo "🚀 CORA-Quantum Assistant - Demostración Automática"
echo "Fecha: 1 de octubre de 2025"
echo "Versión: 1.0 - Prototipo Inicial"
echo

# Verificar si existe entorno virtual
if [ -f "cora_quantum_env/bin/activate" ]; then
    echo "🐍 Activando entorno virtual..."
    source cora_quantum_env/bin/activate
else
    echo "⚠️  Entorno virtual no encontrado, usando Python del sistema..."
fi

echo
echo "🎯 Iniciando demostración completa..."
python3 main.py --mode demo

echo
echo "📊 Ejecutando ejemplos prácticos..."
python3 examples/practical_examples.py

echo
echo "🔍 Verificando integración de componentes..."
python3 verify_integration.py

echo
echo "✅ Demostración completada!"
echo
echo "Para modo interactivo: python3 main.py --mode interactive"
echo "Para configuración: python3 config.py"