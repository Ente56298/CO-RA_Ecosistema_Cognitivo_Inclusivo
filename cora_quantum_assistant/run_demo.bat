@echo off
echo "🚀 CORA-Quantum Assistant - Demostración Automática"
echo "Fecha: 1 de octubre de 2025"
echo "Versión: 1.0 - Prototipo Inicial"
echo.

REM Verificar si existe entorno virtual
if exist "cora_quantum_env\Scripts\activate.bat" (
    echo "🐍 Activando entorno virtual..."
    call cora_quantum_env\Scripts\activate.bat
) else (
    echo "⚠️  Entorno virtual no encontrado, usando Python del sistema..."
)

echo.
echo "🎯 Iniciando demostración completa..."
python main.py --mode demo

echo.
echo "📊 Ejecutando ejemplos prácticos..."
python examples/practical_examples.py

echo.
echo "🔍 Verificando integración de componentes..."
python verify_integration.py

echo.
echo "✅ Demostración completada!"
echo.
echo "Para modo interactivo: python main.py --mode interactive"
echo "Para configuración: python config.py"
pause