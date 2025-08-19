@echo off
echo.
echo 🎯 CO-RA ESCANEO MAESTRO - EJECUCION RAPIDA
echo ==========================================
echo.
echo Configurando permisos de PowerShell...
powershell -Command "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force"

echo.
echo Ejecutando escaneo maestro...
echo (Esto puede tomar varios minutos dependiendo del tamaño de tus discos)
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0Escaneo-Maestro.ps1" -IgnorarOcultas

echo.
echo ✅ Escaneo completado!
echo 📁 Revisa los reportes en: %USERPROFILE%\Desktop\StorageReports\
echo.
pause