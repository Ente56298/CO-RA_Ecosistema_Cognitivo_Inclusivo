@echo off
echo === MONITOREO DE UNIDAD D: - %date% %time% === >> log_monitoreo_d.txt
echo Verificando estado de la unidad D: >> log_monitoreo_d.txt

REM Verificar espacio disponible
echo Espacio disponible en D: >> log_monitoreo_d.txt
dir D: | find "bytes libres" >> log_monitoreo_d.txt

REM Verificar archivos críticos
if exist "D:\DUPLICADOS.py" (
    echo Archivo DUPLICADOS.py encontrado >> log_monitoreo_d.txt
) else (
    echo *** ALERTA: Archivo DUPLICADOS.py NO encontrado *** >> log_monitoreo_d.txt
)

if exist "D:\MediaID.bin" (
    echo Archivo MediaID.bin encontrado >> log_monitoreo_d.txt
) else (
    echo *** ALERTA: Archivo MediaID.bin NO encontrado *** >> log_monitoreo_d.txt
)

REM Contar archivos temporales
echo Archivos .tmp encontrados: >> log_monitoreo_d.txt
dir "D:\*.tmp" /s /b 2>nul | find /c /v "" >> log_monitoreo_d.txt

echo. >> log_monitoreo_d.txt
echo === FIN DEL MONITOREO === >> log_monitoreo_d.txt
echo. >> log_monitoreo_d.txt