@echo off
echo.
echo 🏗️  CO-RA CONSOLIDADOR DE MONOREPO
echo =====================================
echo.
echo Este script organizará tu proyecto disperso en una estructura monorepo modular
echo.
echo 💡 Opciones disponibles:
echo    1. Simulación (recomendado primero)
echo    2. Copiar archivos (mantiene originales)
echo    3. Mover archivos (reorganiza completamente)
echo.

set /p "option=Selecciona opción (1/2/3): "

if "%option%"=="1" (
    echo.
    echo 🔍 Ejecutando simulación...
    powershell -ExecutionPolicy Bypass -File "%~dp0Consolidar-Monorepo.ps1" -DryRun
) else if "%option%"=="2" (
    echo.
    echo 📋 ¿En qué carpeta está tu proyecto?
    set /p "projectPath=Ruta completa (ej: A:\wamp64\www\mi_proyecto): "
    echo.
    echo 📂 Copiando archivos...
    powershell -ExecutionPolicy Bypass -File "%~dp0Consolidar-Monorepo.ps1" -Root "%projectPath%"
) else if "%option%"=="3" (
    echo.
    echo ⚠️  ADVERTENCIA: Esta opción MOVERÁ los archivos originales
    echo    Asegúrate de tener un respaldo antes de continuar
    echo.
    set /p "confirm=¿Estás seguro? (S/N): "
    if /i "%confirm%"=="S" (
        echo.
        echo 📋 ¿En qué carpeta está tu proyecto?
        set /p "projectPath=Ruta completa (ej: A:\wamp64\www\mi_proyecto): "
        echo.
        echo 🚚 Moviendo archivos...
        powershell -ExecutionPolicy Bypass -File "%~dp0Consolidar-Monorepo.ps1" -Root "%projectPath%" -Move
    ) else (
        echo Operación cancelada.
    )
) else (
    echo Opción no válida.
)

echo.
echo ✅ Proceso completado. Revisa los resultados.
echo 📄 Ver migration_report.json para detalles completos.
echo.
pause