<#
    Programar-Auditoria.ps1
    Configura tarea programada para auditoría automática semanal
    Parte del ecosistema CO-RA
#>

[CmdletBinding()]
param(
    [string]$ScriptPath = "$PSScriptRoot\Auditoria-Almacenamiento.ps1",
    [string]$TaskName = "CO-RA-MonitoreoEspacioDiscos",
    [int]$ThresholdGB = 10,
    [string]$OutputDir = "$env:USERPROFILE\Desktop\StorageReports",
    [string[]]$Drives = @('C','D','G','H','I'),
    [string]$DayOfWeek = "Monday",
    [string]$Time = "09:00"
)

Write-Host @"
⏰ CO-RA Programador de Auditoría
   Configurando monitoreo automático semanal
"@ -ForegroundColor Cyan

# Verificar que el script existe
if (-not (Test-Path $ScriptPath)) {
    Write-Error "Script no encontrado: $ScriptPath"
    exit 1
}

# Construir argumentos para el script
$drivesArg = ($Drives -join ',')
$arguments = "-NoProfile -WindowStyle Hidden -File `"$ScriptPath`" -Drives $drivesArg -ThresholdGB $ThresholdGB -OutputDir `"$OutputDir`""

Write-Host "📋 Configuración de la tarea:" -ForegroundColor Yellow
Write-Host "   Nombre: $TaskName" -ForegroundColor White
Write-Host "   Script: $ScriptPath" -ForegroundColor White
Write-Host "   Frecuencia: Semanal, $DayOfWeek a las $Time" -ForegroundColor White
Write-Host "   Unidades: $drivesArg" -ForegroundColor White
Write-Host "   Umbral: $ThresholdGB GB" -ForegroundColor White
Write-Host "   Reportes: $OutputDir" -ForegroundColor White

try {
    # Eliminar tarea existente si existe
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "🗑️  Eliminando tarea existente..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Crear nueva tarea
    Write-Host "⚙️  Creando nueva tarea programada..." -ForegroundColor Cyan
    
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $arguments
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $Time
    
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
    
    $task = Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "CO-RA: Audita espacio en disco y papelera por unidad automáticamente"
    
    Write-Host "✅ Tarea programada creada exitosamente!" -ForegroundColor Green
    Write-Host "📅 Próxima ejecución: $((Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo).NextRunTime)" -ForegroundColor Green
    
    # Mostrar información de la tarea
    Write-Host "`n📋 Información de la tarea:" -ForegroundColor Cyan
    Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State, @{n='NextRun';e={(Get-ScheduledTaskInfo $_).NextRunTime}} | Format-Table -AutoSize
    
    Write-Host "💡 Para ejecutar manualmente: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
    Write-Host "🗑️  Para eliminar: Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
    
} catch {
    Write-Error "Error configurando la tarea programada: $($_.Exception.Message)"
    exit 1
}

Write-Host "`n🛡️  Monitoreo automático CO-RA configurado correctamente" -ForegroundColor Green