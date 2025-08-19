<# 
    Auditoria-Almacenamiento.ps1
    Herramienta de auditoría para el Plan de Emergencia CO-RA
    - No modifica nada (solo lectura y reporte)
    - Protege archivos borrados: NO vacía papelera
    - Integrado con el ecosistema de respaldo ENTE56
#>

[CmdletBinding()]
param(
    [string[]]$Drives,                      # Ej: "C","D","G","H","I"
    [int]$ThresholdGB = 10,                 # Alerta por debajo de X GB libres
    [int]$TopN = 20,                        # Top de archivos más grandes por unidad en alerta
    [string]$OutputDir = "$env:USERPROFILE\Desktop\StorageReports",
    [switch]$IncluirRemovibles              # Incluye unidades removibles si se indica
)

function Format-Size {
    param([long]$Bytes)
    if ($Bytes -ge 1TB) { "{0:N2} TB" -f ($Bytes/1TB) }
    elseif ($Bytes -ge 1GB) { "{0:N2} GB" -f ($Bytes/1GB) }
    elseif ($Bytes -ge 1MB) { "{0:N2} MB" -f ($Bytes/1MB) }
    else { "{0:N0} B" -f $Bytes }
}

function Get-RecycleBinSize {
    param([string]$Root) # Ej: "C:\"
    $path = Join-Path $Root '$Recycle.Bin'
    try {
        if (Test-Path -LiteralPath $path) {
            $sum = (Get-ChildItem -LiteralPath $path -Force -ErrorAction SilentlyContinue |
                Get-ChildItem -Force -Recurse -File -ErrorAction SilentlyContinue |
                Measure-Object -Property Length -Sum).Sum
            if (-not $sum) { 0 } else { [long]$sum }
        } else { 0 }
    } catch { 0 }
}

function Get-LogicalDrives {
    param([switch]$IncludeRemovable)
    $all = Get-CimInstance Win32_LogicalDisk | Where-Object {
        $_.DriveType -in @(3, ($IncludeRemovable.IsPresent ? 2 : -1)) # 3=fijo, 2=removible
    }
    if ($PSBoundParameters.ContainsKey('Drives') -and $script:Drives) {
        $all = $all | Where-Object { $script:Drives -contains ($_.DeviceID.TrimEnd(':')) }
    }
    return $all
}

# Banner CO-RA
Write-Host @"
🛡️  CO-RA Auditoria de Almacenamiento
    Plan de Emergencia - Rescate ENTE56
    Solo lectura - Protege archivos borrados
"@ -ForegroundColor Cyan

# Preparación de salida
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$null = New-Item -ItemType Directory -Path $OutputDir -Force -ErrorAction SilentlyContinue

# 1) Inventario de unidades
$logical = Get-LogicalDrives -IncludeRemovable:$IncluirRemovibles
if (-not $logical) {
    Write-Warning "No se encontraron unidades según los filtros especificados."
    exit 1
}

$report = foreach ($d in $logical) {
    $totalB = [long]$d.Size
    $freeB  = [long]$d.FreeSpace
    $usedB  = $totalB - $freeB
    $rbB    = Get-RecycleBinSize -Root ($d.DeviceID + "\")
    [pscustomobject]@{
        Drive          = $d.DeviceID
        Label          = $d.VolumeName
        FileSystem     = $d.FileSystem
        TotalBytes     = $totalB
        FreeBytes      = $freeB
        UsedBytes      = $usedB
        PercentFree    = if ($totalB -gt 0) { [math]::Round(($freeB/$totalB)*100,2) } else { 0 }
        RecycleBinB    = $rbB
        RecycleBinText = Format-Size $rbB
        TotalText      = Format-Size $totalB
        FreeText       = Format-Size $freeB
        UsedText       = Format-Size $usedB
    }
}

$csvPath = Join-Path $OutputDir "inventario_unidades_$timestamp.csv"
$report | Sort-Object Drive | Export-Csv -NoTypeInformation -Encoding UTF8 $csvPath

Write-Host "`n=== Inventario de unidades ===" -ForegroundColor Cyan
$report | Sort-Object Drive | Select-Object Drive,Label,FileSystem,TotalText,FreeText,UsedText,PercentFree,RecycleBinText | Format-Table -AutoSize

# 2) Alertas por poco espacio
$thresholdBytes = [long]$ThresholdGB * 1GB
$alertDrives = $report | Where-Object { $_.FreeBytes -lt $thresholdBytes }

if ($alertDrives) {
    Write-Host "`n=== ALERTAS: Unidades por debajo de $ThresholdGB GB libres ===" -ForegroundColor Yellow
    $alertDrives | Select-Object Drive,FreeText,PercentFree,RecycleBinText | Format-Table -AutoSize
    ($alertDrives | Select-Object Drive,FreeBytes,PercentFree) |
        Export-Csv -NoTypeInformation -Encoding UTF8 (Join-Path $OutputDir "alertas_$timestamp.csv")
} else {
    Write-Host "`nNo hay unidades bajo el umbral de $ThresholdGB GB." -ForegroundColor Green
}

# 3) Diagnóstico detallado SOLO en unidades en alerta
foreach ($a in $alertDrives) {
    $root = $a.Drive + "\"
    $driveSafe = $a.Drive.TrimEnd(':')
    $topFilesPath = Join-Path $OutputDir "top_archivos_${driveSafe}_$timestamp.csv"
    $byExtPath    = Join-Path $OutputDir "por_extension_${driveSafe}_$timestamp.csv"

    Write-Host "`n--- Diagnóstico en $($a.Drive) ---" -ForegroundColor Magenta
    Write-Host "Papelera: $($a.RecycleBinText). Sugerencia: evaluar recuperación antes de vaciar." -ForegroundColor DarkGray

    # Top archivos más grandes
    try {
        Write-Host "Buscando top $TopN archivos más grandes..." -ForegroundColor DarkCyan
        Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue |
            Sort-Object Length -Descending |
            Select-Object -First $TopN FullName,@{n='Size';e={Format-Size $_.Length}},Length,LastWriteTime |
            Tee-Object -Variable topFiles |
            Export-Csv -NoTypeInformation -Encoding UTF8 $topFilesPath
        $topFiles | Format-Table -AutoSize
    } catch {
        Write-Warning "No se pudo enumerar archivos en $($a.Drive): $($_.Exception.Message)"
    }

    # Acumulado por extensión
    try {
        Write-Host "Resumiendo por extensión..." -ForegroundColor DarkCyan
        Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue |
            Group-Object { $_.Extension.ToLower() } |
            ForEach-Object {
                [pscustomobject]@{
                    Extension = if ($_.Name) { $_.Name } else { '(sin extensión)' }
                    Count     = $_.Count
                    Bytes     = ($_.Group | Measure-Object Length -Sum).Sum
                }
            } |
            Sort-Object Bytes -Descending |
            Select-Object Extension,Count,@{n='Size';e={Format-Size $_.Bytes}},Bytes |
            Tee-Object -Variable byExt |
            Export-Csv -NoTypeInformation -Encoding UTF8 $byExtPath
        $byExt | Select-Object -First 15 | Format-Table -AutoSize
    } catch {
        Write-Warning "No se pudo agrupar por extensión en $($a.Drive): $($_.Exception.Message)"
    }
}

Write-Host "`n🛡️  Reportes CO-RA guardados en: $OutputDir" -ForegroundColor Cyan
Write-Host "📋 Próximo paso: Revisar alertas y planificar rescate según PLAN_EMERGENCIA.md" -ForegroundColor Green

# Código de salida no-cero si hubo alertas
if ($alertDrives) { exit 2 } else { exit 0 }