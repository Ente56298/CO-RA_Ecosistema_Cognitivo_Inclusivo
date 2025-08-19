# 🗺️ Plan de Integración Virtual Display Manager (VDM) - CO•RA

## 🎯 Objetivo

Implementar acceso remoto granular por roles usando VDM para operación distribuida de TenancingoLive, permitiendo que cada operador acceda solo a su módulo específico.

## 📋 Plan de Implementación Paso a Paso

### **FASE 1: Preparación del Servidor** 🖥️

#### 1.1 Instalación Base
```powershell
# Crear estructura de directorios
New-Item -ItemType Directory -Path "C:\VDM_Server" -Force
New-Item -ItemType Directory -Path "C:\VDM_Server\profiles" -Force
New-Item -ItemType Directory -Path "C:\VDM_Server\logs" -Force

# Descargar VDM 2.5
# URL: http://ynea.futureware.at/cgi-bin/virtual_display_manager.pl
# Extraer en C:\VDM_Server\
```

#### 1.2 Configuración de Roles
| Rol | Responsabilidad | Puerto VDM | Usuario |
|-----|----------------|------------|---------|
| `stream_op` | Control de streaming (FFmpeg/OBS) | 5000 | stream_op |
| `bet_admin` | Panel de apuestas y cuotas | 5001 | bet_admin |
| `payments` | Dashboard de transacciones | 5002 | payments |
| `support` | Chat CRM y soporte | 5003 | support |
| `monitor` | Supervisión general (solo lectura) | 5004 | monitor |

### **FASE 2: Configuración del Servidor VDM** ⚙️

#### 2.1 Configuración Principal
```batch
# Ejecutar Server_Interface.exe
# Configuración en pestaña "Principal":
IP: 0.0.0.0
Puerto base: 5000
Sincronización portapapeles: Habilitado
Compresión: Media
```

#### 2.2 Creación de Usuarios
```batch
# En pestaña "Usuario" crear:
Usuario: stream_op | Clave: St2024!Live | Puerto: 5000
Usuario: bet_admin | Clave: Bt2024!Live | Puerto: 5001  
Usuario: payments  | Clave: Py2024!Live | Puerto: 5002
Usuario: support   | Clave: Sp2024!Live | Puerto: 5003
Usuario: monitor   | Clave: Mt2024!Live | Puerto: 5004
```

#### 2.3 Configuración de Ventanas por Rol

##### **Streaming (stream_op)**
```
URI: ffmpeg.exe::MainWindow::-1
URI: obs64.exe::OBSBasicMainWindow::-1
URI: chrome.exe::StreamingDashboard::-1
Descripción: Control de transmisión en vivo
```

##### **Apuestas (bet_admin)**
```
URI: chrome.exe::AdminPanel::BettingModule::-1
URI: chrome.exe::CuotasManager::-1
URI: chrome.exe::ResultsPanel::-1
Descripción: Gestión de apuestas y cuotas
```

##### **Pagos (payments)**
```
URI: chrome.exe::PaymentsDashboard::-1
URI: chrome.exe::TransactionHistory::-1
URI: chrome.exe::VoucherSystem::-1
Descripción: Procesamiento de pagos y vouchers
```

##### **Soporte (support)**
```
URI: chrome.exe::CRMPanel::-1
URI: chrome.exe::ChatSupport::-1
URI: chrome.exe::UserManagement::-1
Descripción: Atención al cliente y soporte
```

##### **Monitor (monitor)**
```
URI: chrome.exe::SystemDashboard::-1
URI: chrome.exe::LiveStats::-1
URI: chrome.exe::AlertsPanel::-1
Descripción: Supervisión general (solo lectura)
```

### **FASE 3: Configuración de Clientes** 💻

#### 3.1 Instalación Cliente
```powershell
# En cada equipo remoto:
# 1. Instalar VDM_Client.exe
# 2. Crear acceso directo con parámetros:

# Para Streaming:
VDM_Client.exe -server IP_SERVIDOR -port 5000 -user stream_op -pass St2024!Live

# Para Apuestas:
VDM_Client.exe -server IP_SERVIDOR -port 5001 -user bet_admin -pass Bt2024!Live

# Para Pagos:
VDM_Client.exe -server IP_SERVIDOR -port 5002 -user payments -pass Py2024!Live

# Para Soporte:
VDM_Client.exe -server IP_SERVIDOR -port 5003 -user support -pass Sp2024!Live
```

#### 3.2 Perfiles de Conexión
```batch
# Crear archivos .bat para conexión rápida:

# streaming_connect.bat
@echo off
cd "C:\VDM_Client"
VDM_Client.exe -server 192.168.1.100 -port 5000 -user stream_op -pass St2024!Live -profile streaming

# betting_connect.bat
@echo off
cd "C:\VDM_Client"
VDM_Client.exe -server 192.168.1.100 -port 5001 -user bet_admin -pass Bt2024!Live -profile betting
```

### **FASE 4: Configuración de Seguridad** 🛡️

#### 4.1 Firewall Windows
```powershell
# Abrir puertos específicos
New-NetFirewallRule -DisplayName "VDM Streaming" -Direction Inbound -Port 5000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "VDM Betting" -Direction Inbound -Port 5001 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "VDM Payments" -Direction Inbound -Port 5002 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "VDM Support" -Direction Inbound -Port 5003 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "VDM Monitor" -Direction Inbound -Port 5004 -Protocol TCP -Action Allow
```

#### 4.2 Restricciones de IP
```batch
# En VDM Server, configurar IPs permitidas por rol:
stream_op: 192.168.1.10, 192.168.1.11
bet_admin: 192.168.1.20, 192.168.1.21
payments: 192.168.1.30
support: 192.168.1.40, 192.168.1.41
monitor: 192.168.1.50-55
```

### **FASE 5: Scripts de Automatización** 🤖

#### 5.1 Inicio Automático del Servidor
```batch
# vdm_server_start.bat
@echo off
echo Iniciando VDM Server para TenancingoLive...
cd "C:\VDM_Server"

# Iniciar servidor con configuración
start "VDM Server" server_process_console.exe -config "profiles\tenancingo_config.ini"

# Verificar inicio
timeout /t 5
tasklist | find "server_process_console.exe" > nul
if %errorlevel% == 0 (
    echo ✅ VDM Server iniciado correctamente
) else (
    echo ❌ Error iniciando VDM Server
)
```

#### 5.2 Monitoreo de Conexiones
```powershell
# monitor_vdm.ps1
$ports = @(5000, 5001, 5002, 5003, 5004)
$roles = @("Streaming", "Betting", "Payments", "Support", "Monitor")

for ($i = 0; $i -lt $ports.Length; $i++) {
    $connections = netstat -an | Select-String ":$($ports[$i])" | Measure-Object
    Write-Host "$($roles[$i]) (Puerto $($ports[$i])): $($connections.Count) conexiones activas"
}
```

### **FASE 6: Procedimientos Operativos** 📋

#### 6.1 Inicio Diario
```batch
# 1. Técnico en servidor ejecuta:
vdm_server_start.bat

# 2. Abrir aplicaciones principales:
start chrome.exe --new-window "http://localhost/admin"
start chrome.exe --new-window "http://localhost/betting"
start chrome.exe --new-window "http://localhost/payments"

# 3. Operadores remotos ejecutan sus .bat de conexión
```

#### 6.2 Monitoreo Continuo
```powershell
# Cada 15 minutos ejecutar:
powershell -File "C:\VDM_Server\monitor_vdm.ps1"

# Log de actividad:
Get-Date | Out-File "C:\VDM_Server\logs\activity.log" -Append
```

### **FASE 7: Plan de Contingencia** 🚨

#### 7.1 Reinicio de Emergencia
```batch
# emergency_restart.bat
@echo off
echo 🚨 Reinicio de emergencia VDM...

# Terminar procesos
taskkill /f /im server_process_console.exe 2>nul
timeout /t 3

# Reiniciar
cd "C:\VDM_Server"
start "VDM Emergency" server_process_console.exe -config "profiles\emergency_config.ini"

echo ✅ VDM reiniciado en modo emergencia
```

#### 7.2 Respaldo de Configuración
```powershell
# backup_vdm_config.ps1
$backupPath = "C:\VDM_Server\backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupPath -Force

# Copiar configuraciones
Copy-Item "C:\VDM_Server\profiles\*" $backupPath -Recurse
Copy-Item "C:\VDM_Server\*.ini" $backupPath

Write-Host "✅ Configuración respaldada en: $backupPath"
```

## 📊 Matriz de URIs por Módulo TenancingoLive

### **Streaming Module**
```
ffmpeg.exe::ConsoleWindowClass::-1
obs64.exe::Qt5QWindowIcon::OBSBasicMainWindow::-1
chrome.exe::Chrome_WidgetWin_1::StreamControl::-1
```

### **Betting Module**
```
chrome.exe::Chrome_WidgetWin_1::BettingPanel::-1
chrome.exe::Chrome_WidgetWin_1::OddsManager::-1
chrome.exe::Chrome_WidgetWin_1::ResultsInput::-1
```

### **Payments Module**
```
chrome.exe::Chrome_WidgetWin_1::PaymentsDashboard::-1
chrome.exe::Chrome_WidgetWin_1::VoucherProcessor::-1
chrome.exe::Chrome_WidgetWin_1::TransactionLog::-1
```

### **Support Module**
```
chrome.exe::Chrome_WidgetWin_1::CRMInterface::-1
chrome.exe::Chrome_WidgetWin_1::LiveChat::-1
chrome.exe::Chrome_WidgetWin_1::UserAdmin::-1
```

## 🔧 Comandos de Diagnóstico

### **Verificar Estado del Servidor**
```powershell
# Estado de procesos VDM
Get-Process | Where-Object {$_.ProcessName -like "*vdm*" -or $_.ProcessName -like "*server_process*"}

# Puertos en uso
netstat -an | Select-String ":500[0-4]"

# Conexiones activas por puerto
netstat -an | Select-String "ESTABLISHED" | Select-String ":500[0-4]"
```

### **Logs de Actividad**
```batch
# Ver últimas conexiones
type "C:\VDM_Server\logs\connections.log" | find /i "$(date /t)"

# Errores recientes
type "C:\VDM_Server\logs\errors.log" | find /i "error"
```

## 📈 Métricas de Rendimiento

### **KPIs a Monitorear**
- Tiempo de respuesta por rol (< 100ms)
- Conexiones simultáneas por puerto
- Uptime del servidor VDM (> 99.5%)
- Errores de conexión por día (< 5)

### **Dashboard de Monitoreo**
```html
<!-- Integrar en panel administrativo -->
<div id="vdm-status">
    <div class="role-status" data-role="streaming">Streaming: ✅</div>
    <div class="role-status" data-role="betting">Apuestas: ✅</div>
    <div class="role-status" data-role="payments">Pagos: ✅</div>
    <div class="role-status" data-role="support">Soporte: ✅</div>
</div>
```

---

## ✅ Checklist de Implementación

### **Pre-implementación**
- [ ] Servidor Windows preparado
- [ ] VDM 2.5 descargado
- [ ] Puertos 5000-5004 disponibles
- [ ] Equipos cliente identificados
- [ ] Credenciales de acceso definidas

### **Implementación**
- [ ] VDM Server instalado y configurado
- [ ] Usuarios y roles creados
- [ ] URIs de ventanas configuradas
- [ ] Clientes instalados y probados
- [ ] Firewall configurado
- [ ] Scripts de automatización creados

### **Post-implementación**
- [ ] Pruebas de conectividad por rol
- [ ] Documentación de operadores entregada
- [ ] Plan de contingencia probado
- [ ] Monitoreo configurado
- [ ] Respaldos programados

---

*Plan de integración VDM para operación distribuida CO•RA* 🗺️