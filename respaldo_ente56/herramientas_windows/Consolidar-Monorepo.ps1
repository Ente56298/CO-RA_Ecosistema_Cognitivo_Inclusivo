<#
    Consolidar-Monorepo.ps1
    Herramienta CO-RA para consolidar proyectos dispersos en estructura monorepo
    Organiza automáticamente archivos por tipo y función
#>

param(
    [string]$Root = ".",
    [switch]$Move,          # Si se incluye, mueve en lugar de copiar
    [switch]$DryRun         # Simula sin escribir cambios
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host @"
🏗️  CO-RA CONSOLIDADOR DE MONOREPO
   Organizando proyecto en estructura modular
"@ -ForegroundColor Cyan

function New-Dir($p) { 
    if (-not (Test-Path $p)) { 
        if (-not $DryRun) { New-Item -ItemType Directory -Path $p | Out-Null }
        Write-Host "📁 Creando: $p" -ForegroundColor Green
    }
}

function CopyOrMove($src, $dst) {
    if ($DryRun) { 
        Write-Host "[SIMULACIÓN] $($Move ? 'MOVER' : 'COPIAR') $src -> $dst" -ForegroundColor Yellow
        return 
    }
    
    New-Dir (Split-Path $dst)
    
    try {
        if ($Move) { 
            Move-Item -LiteralPath $src -Destination $dst -Force -ErrorAction Stop 
        } else { 
            Copy-Item -LiteralPath $src -Destination $dst -Force -ErrorAction Stop 
        }
        Write-Host "✅ $($Move ? 'Movido' : 'Copiado'): $(Split-Path $src -Leaf)" -ForegroundColor Green
    } catch {
        Write-Warning "❌ Error: $($_.Exception.Message)"
        throw
    }
}

function Map-Files($patterns, $target) {
    $results = @()
    foreach ($pattern in $patterns) {
        Get-ChildItem -LiteralPath $Root -Recurse -File -Include $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            $results += [PSCustomObject]@{ 
                source = $_.FullName
                dest = Join-Path $target $_.Name
                type = "file"
            }
        }
    }
    return $results
}

function Map-Folders($folderNames, $target) {
    $results = @()
    foreach ($folderName in $folderNames) {
        $folderPath = Join-Path $Root $folderName
        if (Test-Path $folderPath) {
            $results += [PSCustomObject]@{ 
                source = $folderPath
                dest = Join-Path $target $folderName
                type = "folder"
            }
        }
    }
    return $results
}

# 1) Estructura objetivo del monorepo
Write-Host "`n📋 Creando estructura de monorepo..." -ForegroundColor Yellow

$structure = @{
    "apps/backend-php"     = Join-Path $Root "apps/backend-php"
    "apps/backend-node"    = Join-Path $Root "apps/backend-node"  
    "apps/frontend"        = Join-Path $Root "apps/frontend"
    "workers/python"       = Join-Path $Root "workers/python"
    "infra/nginx"          = Join-Path $Root "infra/nginx"
    "infra/ffmpeg"         = Join-Path $Root "infra/ffmpeg"
    "infra/database"       = Join-Path $Root "infra/database"
    "modules/streaming"    = Join-Path $Root "modules/streaming"
    "modules/webrtc"       = Join-Path $Root "modules/webrtc"
    "public"               = Join-Path $Root "public"
    "docs"                 = Join-Path $Root "docs"
    "config"               = Join-Path $Root "config"
    "legacy"               = Join-Path $Root "legacy"
    "tools"                = Join-Path $Root "tools"
}

$structure.Values | ForEach-Object { New-Dir $_ }

# 2) Plan de migración
Write-Host "`n🗂️  Planificando migración de archivos..." -ForegroundColor Yellow

$migrationPlan = @()

# Documentación
$migrationPlan += Map-Files @("*.md", "*.txt") $structure["docs"]

# Backend PHP
$phpFiles = @(
    "*.php", "index.php", "login.php", "admin*.php", "secure_*.php", 
    "streaming_*.php", "function_*.php", "api.php", "registration.php"
)
$migrationPlan += Map-Files $phpFiles $structure["apps/backend-php"]

# Configuración PHP
$configFiles = @("config*.php", "*.config.php", "session_config.php")
$migrationPlan += Map-Files $configFiles $structure["config"]

# Backend Node.js
$nodeFiles = @("package.json", "*.js", "*.ts", "*_api.js", "*_cron.js")
$migrationPlan += Map-Files $nodeFiles $structure["apps/backend-node"]

# Workers Python
$pythonFiles = @("*.py", "requirements.txt")
$migrationPlan += Map-Files $pythonFiles $structure["workers/python"]

# Base de datos
$dbFiles = @("*.sql", "setup_database.php", "migrate_database.php")
$migrationPlan += Map-Files $dbFiles $structure["infra/database"]

# Assets públicos
$publicFolders = @("css", "js", "img", "images", "video", "admin", "live", "livestream")
$migrationPlan += Map-Folders $publicFolders $structure["public"]

$publicFiles = @("*.html", "*.htm", ".htaccess*", "*.htaccess")
$migrationPlan += Map-Files $publicFiles $structure["public"]

# Infraestructura
$migrationPlan += Map-Folders @("nginx-rtmp", "nginx") $structure["infra/nginx"]
$migrationPlan += Map-Folders @("ffmpeg", "FFmpeg-master") $structure["infra/ffmpeg"]

# Módulos de streaming
$streamingFolders = @("videowhisper", "videowhisper-live-streaming-integration")
$migrationPlan += Map-Folders $streamingFolders $structure["modules/webrtc"]

# Frontend
$migrationPlan += Map-Folders @("tenancingo_react") $structure["apps/frontend"]

# Legacy
$legacyFolders = @("MonaServer_Win64", "red5-flex-streamer", "GoldenX-CASINO-SITE", "rtpm")
$migrationPlan += Map-Folders $legacyFolders $structure["legacy"]

# Variables de entorno
$envFiles = @(".env*", "*.env")
$migrationPlan += Map-Files $envFiles $structure["config"]

# 3) Ejecutar migración
Write-Host "`n🚀 Ejecutando migración..." -ForegroundColor Yellow

$report = @()
$processed = @{}

foreach ($item in $migrationPlan) {
    # Evitar duplicados
    $key = "$($item.source)->$($item.dest)"
    if ($processed.ContainsKey($key)) { continue }
    $processed[$key] = $true
    
    try {
        if (Test-Path $item.source) {
            Write-Host "📦 $($item.source) -> $($item.dest)" -ForegroundColor DarkCyan
            
            if ($item.type -eq "folder") {
                if (-not $DryRun) {
                    if ($Move) {
                        Move-Item -LiteralPath $item.source -Destination $item.dest -Force
                    } else {
                        Copy-Item -LiteralPath $item.source -Destination $item.dest -Recurse -Force
                    }
                }
            } else {
                CopyOrMove $item.source $item.dest
            }
            
            $report += [PSCustomObject]@{ 
                action = ($Move ? 'move' : 'copy')
                source = $item.source
                dest = $item.dest
                type = $item.type
                status = 'success'
                error = $null
            }
        }
    } catch {
        Write-Warning "❌ Error procesando $($item.source): $($_.Exception.Message)"
        $report += [PSCustomObject]@{ 
            action = ($Move ? 'move' : 'copy')
            source = $item.source
            dest = $item.dest
            type = $item.type
            status = 'error'
            error = $_.Exception.Message
        }
    }
}

# 4) Consolidar variables de entorno
Write-Host "`n🔧 Consolidando configuración..." -ForegroundColor Yellow

try {
    $envSample = Join-Path $structure["config"] ".env.sample"
    $envVars = @{}
    
    # Buscar archivos .env existentes
    Get-ChildItem $structure["config"] -File -Include ".env*" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "📄 Procesando: $($_.Name)" -ForegroundColor DarkGray
        
        Get-Content $_.FullName -ErrorAction SilentlyContinue | Where-Object { 
            $_ -match "^\s*[^#]+\s*=\s*.+$" 
        } | ForEach-Object {
            $parts = $_ -split "=", 2
            if ($parts.Length -eq 2) {
                $key = $parts[0].Trim()
                if (-not $envVars.ContainsKey($key)) { 
                    $envVars[$key] = "<CONFIGURAR_VALOR>" 
                }
            }
        }
    }
    
    if (-not $DryRun -and $envVars.Count -gt 0) {
        "# Plantilla de variables de entorno - CO-RA Monorepo" | Out-File $envSample -Encoding utf8
        "# Completa los valores según tu entorno" | Out-File $envSample -Append -Encoding utf8
        "" | Out-File $envSample -Append -Encoding utf8
        
        $envVars.Keys | Sort-Object | ForEach-Object { 
            "$_=$($envVars[$_])" | Out-File $envSample -Append -Encoding utf8
        }
    }
    
    Write-Host "✅ Configuración consolidada: $envSample" -ForegroundColor Green
    
} catch {
    Write-Warning "⚠️  No se pudo consolidar .env: $($_.Exception.Message)"
}

# 5) Crear archivos de configuración del monorepo
if (-not $DryRun) {
    # README principal
    $mainReadme = Join-Path $Root "README.md"
    if (-not (Test-Path $mainReadme)) {
        @"
# 🏗️ Proyecto Consolidado - Monorepo

## 📂 Estructura

- **apps/** - Aplicaciones principales
  - **backend-php/** - API y lógica PHP
  - **backend-node/** - Servicios Node.js
  - **frontend/** - Interfaces de usuario
- **workers/** - Procesos en segundo plano
- **infra/** - Infraestructura y servicios
- **modules/** - Módulos reutilizables
- **public/** - Assets públicos
- **docs/** - Documentación
- **config/** - Configuración centralizada
- **legacy/** - Código heredado
- **tools/** - Herramientas de desarrollo

## 🚀 Inicio Rápido

1. Configurar variables de entorno:
   \`\`\`bash
   cp config/.env.sample config/.env
   # Editar config/.env con tus valores
   \`\`\`

2. Ver documentación específica en cada carpeta

## 📋 Migración

Este proyecto fue consolidado automáticamente usando CO-RA Consolidador.
Ver \`migration_report.json\` para detalles de la migración.
"@ | Out-File $mainReadme -Encoding utf8
    }
    
    # .gitignore
    $gitignore = Join-Path $Root ".gitignore"
    if (-not (Test-Path $gitignore)) {
        @"
# Variables de entorno
.env
.env.local
.env.production
config/.env

# Logs
*.log
logs/

# Dependencias
node_modules/
vendor/

# Build
dist/
build/
public/build/

# Cache
.cache/
*.cache

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Temporales
temp/
tmp/
"@ | Out-File $gitignore -Encoding utf8
    }
}

# 6) Generar reporte final
$reportPath = Join-Path $Root "migration_report.json"
if (-not $DryRun) {
    $finalReport = @{
        timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        mode = if ($Move) { "move" } else { "copy" }
        total_items = $report.Count
        successful = ($report | Where-Object { $_.status -eq 'success' }).Count
        failed = ($report | Where-Object { $_.status -eq 'error' }).Count
        structure_created = $structure.Keys
        items = $report
    }
    
    $finalReport | ConvertTo-Json -Depth 5 | Out-File $reportPath -Encoding utf8
}

# 7) Resumen final
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "🎉 CONSOLIDACIÓN COMPLETADA" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

Write-Host "📊 Estadísticas:" -ForegroundColor Yellow
Write-Host "   Total elementos: $($report.Count)" -ForegroundColor White
Write-Host "   Exitosos: $(($report | Where-Object { $_.status -eq 'success' }).Count)" -ForegroundColor Green
Write-Host "   Errores: $(($report | Where-Object { $_.status -eq 'error' }).Count)" -ForegroundColor Red

Write-Host "`n📁 Estructura creada:" -ForegroundColor Yellow
$structure.Keys | Sort-Object | ForEach-Object {
    Write-Host "   📂 $_" -ForegroundColor White
}

Write-Host "`n📋 Archivos generados:" -ForegroundColor Yellow
Write-Host "   📄 $reportPath" -ForegroundColor White
Write-Host "   📄 README.md" -ForegroundColor White
Write-Host "   📄 .gitignore" -ForegroundColor White
Write-Host "   📄 config/.env.sample" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n💡 Esto fue una simulación. Ejecuta sin -DryRun para aplicar cambios." -ForegroundColor Yellow
} else {
    Write-Host "`n✅ Monorepo consolidado exitosamente" -ForegroundColor Green
}

Write-Host "`n🛡️  Consolidación CO-RA completada" -ForegroundColor Cyan