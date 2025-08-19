<#
    VDM_SCRIPTS_AUTOMATIZACION.ps1
    Scripts de automatización para Virtual Display Manager
    Parte del ecosistema CO-RA
#>

# Configuración global
$VDM_PATH = "C:\VDM_Server"
$LOG_PATH = "$VDM_PATH\logs"
$BACKUP_PATH = "$VDM_PATH\backups"
$CONFIG_PATH = "$VDM_PATH\profiles"

# Crear directorios si no existen
@($LOG_PATH, $BACKUP_PATH, $CONFIG_PATH) | ForEach-Object {
    if (-not (Test-Path $_)) { New-Item -ItemType Directory -Path $_ -Force | Out-Null }
}

function Write-VDMLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry -ForegroundColor $(if($Level -eq "ERROR"){"Red"} elseif($Level -eq "WARN"){"Yellow"} else{"Green"})
    $logEntry | Out-File "$LOG_PATH\vdm_automation.log" -Append -Encoding UTF8
}

function Start-VDMServer {
    <#
    .SYNOPSIS
    Inicia el servidor VDM con configuración para TenancingoLive
    #>
    
    Write-VDMLog "Iniciando VDM Server para TenancingoLive..."
    
    # Verificar si ya está ejecutándose
    $existing = Get-Process -Name "server_process_console" -ErrorAction SilentlyContinue
    if ($existing) {
        Write-VDMLog "VDM Server ya está ejecutándose (PID: $($existing.Id))" "WARN"
        return $true
    }
    
    try {
        # Cambiar al directorio VDM
        Set-Location $VDM_PATH
        
        # Iniciar servidor
        $process = Start-Process -FilePath "server_process_console.exe" -ArgumentList "-config `"$CONFIG_PATH\tenancingo_config.ini`"" -PassThru -WindowStyle Minimized
        
        # Esperar y verificar inicio
        Start-Sleep -Seconds 5
        
        if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
            Write-VDMLog "✅ VDM Server iniciado correctamente (PID: $($process.Id))"
            return $true
        } else {
            Write-VDMLog "❌ Error: VDM Server no se pudo iniciar" "ERROR"
            return $false
        }
        
    } catch {
        Write-VDMLog "❌ Error iniciando VDM Server: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Stop-VDMServer {
    <#
    .SYNOPSIS
    Detiene el servidor VDM de forma segura
    #>
    
    Write-VDMLog "Deteniendo VDM Server..."
    
    try {
        $processes = Get-Process -Name "server_process_console" -ErrorAction SilentlyContinue
        
        if (-not $processes) {
            Write-VDMLog "VDM Server no está ejecutándose" "WARN"
            return $true
        }
        
        foreach ($process in $processes) {
            Write-VDMLog "Terminando proceso VDM (PID: $($process.Id))"
            $process.CloseMainWindow()
            
            # Esperar cierre graceful
            if (-not $process.WaitForExit(10000)) {
                Write-VDMLog "Forzando cierre del proceso VDM" "WARN"
                $process.Kill()
            }
        }
        
        Write-VDMLog "✅ VDM Server detenido correctamente"
        return $true
        
    } catch {
        Write-VDMLog "❌ Error deteniendo VDM Server: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-VDMConnections {
    <#
    .SYNOPSIS
    Verifica el estado de las conexiones VDM por rol
    #>
    
    Write-VDMLog "Verificando conexiones VDM..."
    
    $ports = @{
        5000 = "Streaming"
        5001 = "Betting" 
        5002 = "Payments"
        5003 = "Support"
        5004 = "Monitor"
    }
    
    $results = @()
    
    foreach ($port in $ports.Keys) {
        try {
            $connections = netstat -an | Select-String ":$port " | Where-Object { $_ -match "ESTABLISHED" }
            $count = ($connections | Measure-Object).Count
            
            $status = @{
                Role = $ports[$port]
                Port = $port
                Connections = $count
                Status = if ($count -gt 0) { "✅ Activo" } else { "⚠️ Sin conexiones" }
            }
            
            $results += New-Object PSObject -Property $status
            Write-VDMLog "$($ports[$port]) (Puerto $port): $count conexiones activas"
            
        } catch {
            Write-VDMLog "Error verificando puerto $port`: $($_.Exception.Message)" "ERROR"
        }
    }
    
    return $results
}

function Backup-VDMConfiguration {
    <#
    .SYNOPSIS
    Crea respaldo de la configuración VDM
    #>
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = "$BACKUP_PATH\config_$timestamp"
    
    Write-VDMLog "Creando respaldo de configuración VDM..."
    
    try {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        
        # Respaldar archivos de configuración
        if (Test-Path "$CONFIG_PATH\*") {
            Copy-Item "$CONFIG_PATH\*" $backupDir -Recurse -Force
            Write-VDMLog "Perfiles copiados a respaldo"
        }
        
        # Respaldar archivos .ini
        Get-ChildItem $VDM_PATH -Filter "*.ini" | ForEach-Object {
            Copy-Item $_.FullName $backupDir -Force
            Write-VDMLog "Configuración $($_.Name) respaldada"
        }
        
        # Crear manifiesto del respaldo
        $manifest = @{
            timestamp = $timestamp
            backup_path = $backupDir
            files_count = (Get-ChildItem $backupDir -Recurse -File).Count
            created_by = $env:USERNAME
        }
        
        $manifest | ConvertTo-Json | Out-File "$backupDir\manifest.json" -Encoding UTF8
        
        Write-VDMLog "✅ Respaldo completado: $backupDir"
        return $backupDir
        
    } catch {
        Write-VDMLog "❌ Error creando respaldo: $($_.Exception.Message)" "ERROR"
        return $null
    }
}

function Restart-VDMEmergency {
    <#
    .SYNOPSIS
    Reinicio de emergencia del servidor VDM
    #>
    
    Write-VDMLog "🚨 Iniciando reinicio de emergencia VDM..." "WARN"
    
    try {
        # Detener servidor actual
        Stop-VDMServer
        
        # Esperar limpieza
        Start-Sleep -Seconds 3
        
        # Iniciar en modo emergencia
        Set-Location $VDM_PATH
        $process = Start-Process -FilePath "server_process_console.exe" -ArgumentList "-config `"$CONFIG_PATH\emergency_config.ini`"" -PassThru -WindowStyle Minimized
        
        Start-Sleep -Seconds 5
        
        if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
            Write-VDMLog "✅ VDM reiniciado en modo emergencia (PID: $($process.Id))"
            return $true
        } else {
            Write-VDMLog "❌ Error en reinicio de emergencia" "ERROR"
            return $false
        }
        
    } catch {
        Write-VDMLog "❌ Error crítico en reinicio de emergencia: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Monitor-VDMHealth {
    <#
    .SYNOPSIS
    Monitoreo continuo de salud del sistema VDM
    #>
    
    Write-VDMLog "Iniciando monitoreo de salud VDM..."
    
    $healthReport = @{
        timestamp = Get-Date
        server_running = $false
        connections = @()
        memory_usage = 0
        cpu_usage = 0
        disk_space = 0
        alerts = @()
    }
    
    try {
        # Verificar proceso servidor
        $serverProcess = Get-Process -Name "server_process_console" -ErrorAction SilentlyContinue
        $healthReport.server_running = $serverProcess -ne $null
        
        if ($serverProcess) {
            $healthReport.memory_usage = [math]::Round($serverProcess.WorkingSet64 / 1MB, 2)
            $healthReport.cpu_usage = $serverProcess.CPU
        }
        
        # Verificar conexiones
        $healthReport.connections = Test-VDMConnections
        
        # Verificar espacio en disco
        $disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
        $healthReport.disk_space = [math]::Round($disk.FreeSpace / 1GB, 2)
        
        # Generar alertas
        if (-not $healthReport.server_running) {
            $healthReport.alerts += "🚨 Servidor VDM no está ejecutándose"
        }
        
        if ($healthReport.memory_usage -gt 500) {
            $healthReport.alerts += "⚠️ Uso de memoria alto: $($healthReport.memory_usage) MB"
        }
        
        if ($healthReport.disk_space -lt 1) {
            $healthReport.alerts += "🚨 Espacio en disco crítico: $($healthReport.disk_space) GB"
        }
        
        $noConnections = ($healthReport.connections | Where-Object { $_.Connections -eq 0 }).Count
        if ($noConnections -gt 2) {
            $healthReport.alerts += "⚠️ Múltiples roles sin conexiones activas"
        }
        
        # Guardar reporte
        $healthReport | ConvertTo-Json -Depth 3 | Out-File "$LOG_PATH\health_$(Get-Date -Format 'yyyyMMdd_HHmmss').json" -Encoding UTF8
        
        # Log alertas
        foreach ($alert in $healthReport.alerts) {
            Write-VDMLog $alert "WARN"
        }
        
        if ($healthReport.alerts.Count -eq 0) {
            Write-VDMLog "✅ Sistema VDM funcionando correctamente"
        }
        
        return $healthReport
        
    } catch {
        Write-VDMLog "❌ Error en monitoreo de salud: $($_.Exception.Message)" "ERROR"
        return $null
    }
}

function Install-VDMService {
    <#
    .SYNOPSIS
    Configura VDM como servicio de Windows (requiere herramientas adicionales)
    #>
    
    Write-VDMLog "Configurando VDM como servicio de Windows..."
    
    $serviceName = "VDM_TenancingoLive"
    $serviceDisplayName = "VDM Server - TenancingoLive"
    $serviceDescription = "Virtual Display Manager para operación distribuida de TenancingoLive"
    
    try {
        # Verificar si el servicio ya existe
        $existingService = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        
        if ($existingService) {
            Write-VDMLog "Servicio VDM ya existe, actualizando configuración..." "WARN"
            Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
        }
        
        # Crear script wrapper para el servicio
        $wrapperScript = @"
@echo off
cd /d "$VDM_PATH"
server_process_console.exe -config "$CONFIG_PATH\tenancingo_config.ini"
"@
        
        $wrapperPath = "$VDM_PATH\vdm_service_wrapper.bat"
        $wrapperScript | Out-File $wrapperPath -Encoding ASCII
        
        Write-VDMLog "✅ Wrapper de servicio creado: $wrapperPath"
        Write-VDMLog "💡 Para completar la instalación del servicio, usar NSSM o sc.exe manualmente"
        
        return $wrapperPath
        
    } catch {
        Write-VDMLog "❌ Error configurando servicio: $($_.Exception.Message)" "ERROR"
        return $null
    }
}

# Funciones de utilidad para operadores
function Get-VDMStatus {
    Write-Host "`n🖥️  ESTADO VDM TENANCINGLIVE" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    
    $connections = Test-VDMConnections
    $connections | Format-Table Role, Port, Connections, Status -AutoSize
    
    $serverRunning = Get-Process -Name "server_process_console" -ErrorAction SilentlyContinue
    if ($serverRunning) {
        Write-Host "🟢 Servidor VDM: ACTIVO (PID: $($serverRunning.Id))" -ForegroundColor Green
    } else {
        Write-Host "🔴 Servidor VDM: INACTIVO" -ForegroundColor Red
    }
}

function Start-VDMDailyOperations {
    Write-Host "`n🚀 INICIANDO OPERACIONES DIARIAS VDM" -ForegroundColor Cyan
    
    # 1. Iniciar servidor VDM
    if (Start-VDMServer) {
        Write-Host "✅ Servidor VDM iniciado" -ForegroundColor Green
    } else {
        Write-Host "❌ Error iniciando servidor VDM" -ForegroundColor Red
        return $false
    }
    
    # 2. Abrir aplicaciones principales
    Write-Host "📱 Abriendo aplicaciones principales..."
    
    try {
        Start-Process "chrome.exe" -ArgumentList "--new-window", "http://localhost/admin" -WindowStyle Minimized
        Start-Process "chrome.exe" -ArgumentList "--new-window", "http://localhost/betting" -WindowStyle Minimized  
        Start-Process "chrome.exe" -ArgumentList "--new-window", "http://localhost/payments" -WindowStyle Minimized
        
        Write-Host "✅ Aplicaciones web iniciadas" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Error abriendo algunas aplicaciones: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # 3. Verificar estado
    Start-Sleep -Seconds 10
    Get-VDMStatus
    
    Write-Host "`n🎯 Sistema listo para operadores remotos" -ForegroundColor Green
    return $true
}

# Exportar funciones principales
Export-ModuleMember -Function Start-VDMServer, Stop-VDMServer, Test-VDMConnections, Backup-VDMConfiguration, Restart-VDMEmergency, Monitor-VDMHealth, Get-VDMStatus, Start-VDMDailyOperations