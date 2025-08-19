<#
    Mover-Archivos-Grandes.ps1
    Herramienta de migración para liberar espacio - CO-RA
    USAR SOLO DESPUÉS DE COMPLETAR EL RESCATE DE EMERGENCIA
#>

[CmdletBinding()]
param(
    [string[]]$SourceDrives = @('D','G','H','I'),
    [string]$DestDrive = 'M',
    [int]$MinSizeMB = 500,
    [int]$OlderThanDays = 60,
    [switch]$DoIt # si no se pasa, solo muestra (WhatIf)
)

Write-Host @"
🚚 CO-RA Migración de Archivos Grandes
   ⚠️  USAR SOLO DESPUÉS DEL RESCATE COMPLETO
   📋 Consultar PLAN_EMERGENCIA.md antes de proceder
"@ -ForegroundColor Yellow

if (-not $DoIt) {
    Write-Host "🔍 MODO SIMULACIÓN - No se moverá nada" -ForegroundColor Cyan
    Write-Host "   Usa -DoIt para ejecutar realmente" -ForegroundColor DarkGray
}

$destRoot = "$DestDrive`:\Migrado_$(Get-Date -Format yyyyMMdd)"

if ($DoIt) {
    $null = New-Item -ItemType Directory -Path $destRoot -Force
    Write-Host "📁 Carpeta destino creada: $destRoot" -ForegroundColor Green
}

$totalCandidatos = 0
$totalSize = 0

foreach ($s in $SourceDrives) {
    $root = "$s`:\"
    if (-not (Test-Path $root)) {
        Write-Warning "Unidad $s no encontrada, omitiendo..."
        continue
    }
    
    Write-Host "`n🔍 Analizando $root ..." -ForegroundColor Cyan
    
    try {
        $candidatos = Get-ChildItem -LiteralPath $root -Recurse -File -Force -ErrorAction SilentlyContinue |
            Where-Object { 
                $_.Length -ge ($MinSizeMB * 1MB) -and 
                $_.LastWriteTime -lt (Get-Date).AddDays(-$OlderThanDays) 
            }

        $driveTotal = ($candidatos | Measure-Object Length -Sum).Sum
        $totalSize += $driveTotal
        $totalCandidatos += $candidatos.Count
        
        Write-Host "   📊 Encontrados: $($candidatos.Count) archivos, $(Format-Size $driveTotal)" -ForegroundColor DarkCyan

        foreach ($f in $candidatos) {
            $rel = $f.FullName.Substring($root.Length)
            $destPath = Join-Path $destRoot "$s\$rel"
            
            if ($DoIt) {
                $null = New-Item -ItemType Directory -Path (Split-Path $destPath) -Force -ErrorAction SilentlyContinue
                try {
                    Move-Item -LiteralPath $f.FullName -Destination $destPath -Force
                    Write-Host "   ✅ Movido: $($f.Name)" -ForegroundColor Green
                } catch {
                    Write-Warning "   ❌ Error moviendo $($f.Name): $($_.Exception.Message)"
                }
            } else {
                Write-Host "   [SIMULACIÓN] $($f.Name) ($(Format-Size $f.Length))" -ForegroundColor DarkGray
            }
        }
    } catch {
        Write-Warning "Error procesando unidad $s`: $($_.Exception.Message)"
    }
}

Write-Host "`n📊 RESUMEN TOTAL:" -ForegroundColor Cyan
Write-Host "   Archivos candidatos: $totalCandidatos" -ForegroundColor White
Write-Host "   Espacio a liberar: $(Format-Size $totalSize)" -ForegroundColor White

if (-not $DoIt) {
    Write-Host "`n💡 Para ejecutar realmente: .\Mover-Archivos-Grandes.ps1 -DoIt" -ForegroundColor Yellow
} else {
    Write-Host "`n✅ Migración completada a: $destRoot" -ForegroundColor Green
}

function Format-Size {
    param([long]$Bytes)
    if ($Bytes -ge 1TB) { "{0:N2} TB" -f ($Bytes/1TB) }
    elseif ($Bytes -ge 1GB) { "{0:N2} GB" -f ($Bytes/1GB) }
    elseif ($Bytes -ge 1MB) { "{0:N2} MB" -f ($Bytes/1MB) }
    else { "{0:N0} B" -f $Bytes }
}