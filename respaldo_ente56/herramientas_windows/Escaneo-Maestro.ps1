<# 
    Escaneo-Maestro.ps1
    🎯 DIAGNÓSTICO COMPLETO CO-RA EN UNA SOLA EJECUCIÓN
    - Auditoría de discos (espacio, papelera, alertas)
    - Localiza carpetas de proyectos por palabras clave
    - Solo lectura: no borra ni mueve nada
#>

[CmdletBinding()]
param(
    [string[]]$Drives = @('C','D','E','F','G','H','I','J','K','L','M','N','A'),
    [string[]]$Keywords = @('proyecto','project','src','dev','repo','github','workspace','tesis','UMED','UnADM','ente56'),
    [int]$ThresholdGB = 10,
    [string]$OutputDir = "$env:USERPROFILE\Desktop\StorageReports",
    [switch]$IgnorarOcultas
)

Write-Host @"
🎯 CO-RA ESCANEO MAESTRO
   Diagnóstico completo en una ejecución
   📊 Auditoría + 🔍 Localización + ⚠️ Alertas
"@ -ForegroundColor Cyan

function Format-Size {
    param([long]$B)
    if ($B -ge 1TB) { "{0:N2} TB" -f ($B/1TB) }
    elseif ($B -ge 1GB) { "{0:N2} GB" -f ($B/1GB) }
    elseif ($B -ge 1MB) { "{0:N2} MB" -f ($B/1MB) }
    else { "{0:N0} B" -f $B }
}

function Get-RecycleBinSize {
    param([string]$Root)
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

function Buscar-Proyectos {
    param(
        [string]$Root,
        [string[]]$Palabras,
        [switch]$SkipHidden
    )
    
    Write-Host "   🔍 Escaneando $Root..." -ForegroundColor DarkGray
    
    try {
        Get-ChildItem -LiteralPath $Root -Directory -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object {
                if ($SkipHidden) {
                    -not (($_.Attributes -band [IO.FileAttributes]::Hidden) -or ($_.Attributes -band [IO.FileAttributes]::System))
                } else { $true }
            } |
            Where-Object {
                $n = $_.Name.ToLower()
                $found = $false
                foreach ($palabra in $Palabras) {
                    if ($n -like "*$($palabra.ToLower())*") {
                        $found = $true
                        break
                    }
                }
                $found
            }
    } catch {
        Write-Warning "Error escaneando $Root`: $($_.Exception.Message)"
    }
}

# Preparar directorio de salida
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$null = New-Item -ItemType Directory -Path $OutputDir -Force -ErrorAction SilentlyContinue

Write-Host "`n📊 PASO 1: Auditoría de unidades..." -ForegroundColor Yellow

# ==== 1) Auditoría de discos ====
$report = foreach ($d in $Drives) {
    $root = "$d`:\"
    if (Test-Path $root) {
        try {
            $drive = Get-PSDrive -Name $d -ErrorAction SilentlyContinue
            if ($drive) {
                $totalB = $drive.Used + $drive.Free
                $freeB  = $drive.Free
                $usedB  = $drive.Used
                $rbB    = Get-RecycleBinSize -Root $root
                
                [pscustomobject]@{
                    Drive          = "$d`:"
                    TotalBytes     = $totalB
                    FreeBytes      = $freeB
                    UsedBytes      = $usedB
                    PercentFree    = if ($totalB -gt 0) { [math]::Round(($freeB/$totalB)*100,2) } else { 0 }
                    RecycleBinB    = $rbB
                    TotalText      = Format-Size $totalB
                    FreeText       = Format-Size $freeB
                    UsedText       = Format-Size $usedB
                    RecycleBinText = Format-Size $rbB
                }
            }
        } catch {
            Write-Warning "Error procesando unidad $d`: $($_.Exception.Message)"
        }
    }
}

$report = $report | Where-Object { $_ -ne $null }
$csvAuditoria = Join-Path $OutputDir "auditoria_$timestamp.csv"
$report | Export-Csv -NoTypeInformation -Encoding UTF8 $csvAuditoria

# Mostrar resumen en pantalla
Write-Host "`n=== INVENTARIO DE UNIDADES ===" -ForegroundColor Cyan
$report | Sort-Object Drive | Select-Object Drive,TotalText,FreeText,UsedText,PercentFree,RecycleBinText | Format-Table -AutoSize

Write-Host "`n⚠️  PASO 2: Detectando alertas..." -ForegroundColor Yellow

# ==== 2) Alertas ====
$thresholdBytes = [long]$ThresholdGB * 1GB
$alertas = $report | Where-Object { $_.FreeBytes -lt $thresholdBytes }
$csvAlertas = Join-Path $OutputDir "alertas_$timestamp.csv"
$alertas | Export-Csv -NoTypeInformation -Encoding UTF8 $csvAlertas

if ($alertas) {
    Write-Host "`n=== 🚨 ALERTAS: Unidades críticas ===" -ForegroundColor Red
    $alertas | Select-Object Drive,FreeText,PercentFree,RecycleBinText | Format-Table -AutoSize
} else {
    Write-Host "`n✅ No hay unidades bajo el umbral de $ThresholdGB GB" -ForegroundColor Green
}

Write-Host "`n🔍 PASO 3: Localizando proyectos..." -ForegroundColor Yellow

# ==== 3) Localización de proyectos ====
$proyectosEncontrados = @()
$totalCarpetas = 0

foreach ($d in $Drives) {
    $root = "$d`:\"
    if (Test-Path $root) {
        Write-Host "📂 Escaneando unidad $d..." -ForegroundColor DarkCyan
        
        $carpetasUnidad = Buscar-Proyectos -Root $root -Palabras $Keywords -SkipHidden:$IgnorarOcultas
        
        foreach ($carpeta in $carpetasUnidad) {
            $proyectosEncontrados += [pscustomobject]@{
                Drive = $d
                Carpeta = $carpeta.FullName
                Nombre = $carpeta.Name
                UltimaMod = $carpeta.LastWriteTime
                Tamaño = try { 
                    $size = (Get-ChildItem -LiteralPath $carpeta.FullName -Recurse -File -ErrorAction SilentlyContinue | 
                             Measure-Object -Property Length -Sum).Sum
                    if ($size) { Format-Size $size } else { "N/A" }
                } catch { "N/A" }
            }
            $totalCarpetas++
        }
        
        Write-Host "   ✅ $($carpetasUnidad.Count) carpetas encontradas en $d" -ForegroundColor Green
    }
}

$csvProyectos = Join-Path $OutputDir "proyectos_$timestamp.csv"
$proyectosEncontrados | Sort-Object Drive,Carpeta | Export-Csv -NoTypeInformation -Encoding UTF8 $csvProyectos

# Mostrar resumen de proyectos
Write-Host "`n=== 🔍 PROYECTOS ENCONTRADOS ===" -ForegroundColor Cyan
Write-Host "Total carpetas: $totalCarpetas" -ForegroundColor White

if ($proyectosEncontrados) {
    # Top 10 más recientes
    Write-Host "`n📅 Top 10 más recientes:" -ForegroundColor Yellow
    $proyectosEncontrados | Sort-Object UltimaMod -Descending | Select-Object -First 10 Drive,Nombre,UltimaMod,Tamaño | Format-Table -AutoSize
    
    # Por unidad
    Write-Host "`n📊 Resumen por unidad:" -ForegroundColor Yellow
    $proyectosEncontrados | Group-Object Drive | Sort-Object Name | ForEach-Object {
        Write-Host "   $($_.Name): $($_.Count) carpetas" -ForegroundColor White
    }
}

# ==== 4) Resumen final ====
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "🎯 RESUMEN EJECUTIVO CO-RA" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

Write-Host "📊 Unidades analizadas: $($report.Count)" -ForegroundColor White
Write-Host "⚠️  Unidades en alerta: $($alertas.Count)" -ForegroundColor $(if ($alertas.Count -gt 0) { "Red" } else { "Green" })
Write-Host "🔍 Proyectos encontrados: $totalCarpetas" -ForegroundColor White

$totalRecycleBin = ($report | Measure-Object RecycleBinB -Sum).Sum
Write-Host "🗑️  Total en papeleras: $(Format-Size $totalRecycleBin)" -ForegroundColor Yellow

Write-Host "`n📁 Reportes generados:" -ForegroundColor Cyan
Write-Host "   📊 $csvAuditoria" -ForegroundColor White
Write-Host "   ⚠️  $csvAlertas" -ForegroundColor White  
Write-Host "   🔍 $csvProyectos" -ForegroundColor White

Write-Host "`n💡 Próximos pasos:" -ForegroundColor Green
if ($alertas) {
    Write-Host "   1. Revisar unidades en alerta crítica" -ForegroundColor Yellow
    Write-Host "   2. Evaluar contenido de papeleras antes de vaciar" -ForegroundColor Yellow
}
Write-Host "   3. Priorizar rescate de proyectos encontrados" -ForegroundColor White
Write-Host "   4. Consultar PLAN_EMERGENCIA.md para siguiente fase" -ForegroundColor White

Write-Host "`n🛡️  Escaneo maestro CO-RA completado" -ForegroundColor Green