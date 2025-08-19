# 🛡️ Herramientas Windows - CO•RA

## 🎯 Propósito

Conjunto de scripts de PowerShell para auditoría y gestión de almacenamiento en Windows, integrados con el Plan de Emergencia CO•RA para rescate de datos ENTE56.

## 📂 Scripts Incluidos

### 🔍 Auditoria-Almacenamiento.ps1
**Función**: Auditoría completa de espacio en disco y papelera
**Características**:
- ✅ Solo lectura - NO modifica archivos
- 🛡️ Protege archivos borrados - NO vacía papelera
- 📊 Inventario completo de unidades
- ⚠️ Alertas por poco espacio libre
- 📈 Análisis detallado de archivos grandes
- 📋 Reportes CSV para seguimiento

**Uso básico**:
```powershell
.\Auditoria-Almacenamiento.ps1 -ThresholdGB 10 -Drives C,D,G,H,I
```

**Parámetros**:
- `-Drives`: Unidades a auditar (ej: C,D,G,H,I)
- `-ThresholdGB`: Umbral de alerta en GB (default: 10)
- `-TopN`: Top archivos más grandes a mostrar (default: 20)
- `-OutputDir`: Carpeta para reportes (default: Desktop\StorageReports)
- `-IncluirRemovibles`: Incluir unidades USB/removibles

### 🚚 Mover-Archivos-Grandes.ps1
**Función**: Migración segura de archivos grandes para liberar espacio
**⚠️ USAR SOLO DESPUÉS DEL RESCATE COMPLETO**

**Uso**:
```powershell
# Simulación (recomendado primero)
.\Mover-Archivos-Grandes.ps1 -SourceDrives D,G,H,I -DestDrive M

# Ejecución real
.\Mover-Archivos-Grandes.ps1 -SourceDrives D,G,H,I -DestDrive M -DoIt
```

### ⏰ Programar-Auditoria.ps1
**Función**: Configura monitoreo automático semanal

**Uso**:
```powershell
.\Programar-Auditoria.ps1 -Drives C,D,G,H,I -ThresholdGB 10
```

## 🚀 Flujo de Trabajo Recomendado

### 1️⃣ Auditoría Inicial
```powershell
# Ejecutar con permisos de administrador
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\Auditoria-Almacenamiento.ps1 -Drives C,D,G,H,I -ThresholdGB 10
```

### 2️⃣ Análisis de Resultados
- Revisar reportes en `Desktop\StorageReports\`
- Identificar unidades en alerta
- Evaluar contenido de papeleras antes de vaciar
- Planificar rescate según criticidad

### 3️⃣ Programar Monitoreo
```powershell
.\Programar-Auditoria.ps1 -Drives C,D,G,H,I
```

### 4️⃣ Migración (Solo después del rescate)
```powershell
# Primero simular
.\Mover-Archivos-Grandes.ps1 -SourceDrives D,G,H,I -DestDrive M

# Luego ejecutar
.\Mover-Archivos-Grandes.ps1 -SourceDrives D,G,H,I -DestDrive M -DoIt
```

## 📊 Reportes Generados

### CSV Files
- `inventario_unidades_YYYYMMDD_HHMMSS.csv`: Inventario completo
- `alertas_YYYYMMDD_HHMMSS.csv`: Unidades con poco espacio
- `top_archivos_X_YYYYMMDD_HHMMSS.csv`: Archivos más grandes por unidad
- `por_extension_X_YYYYMMDD_HHMMSS.csv`: Resumen por tipo de archivo

### Información Incluida
- Espacio total, usado y libre por unidad
- Tamaño de papelera por unidad
- Top archivos más grandes
- Estadísticas por extensión
- Fechas de modificación

## 🛡️ Principios de Seguridad

### ✅ Operaciones Seguras
- Solo lectura por defecto
- Simulación antes de mover archivos
- Preservación de papeleras
- Reportes detallados de cambios

### ⚠️ Precauciones
- Ejecutar con permisos de administrador
- Revisar simulaciones antes de ejecutar
- Mantener respaldos antes de migrar
- No vaciar papeleras sin revisar contenido

## 🔧 Requisitos Técnicos

- **PowerShell**: 5.1 o superior
- **Permisos**: Administrador recomendado
- **Espacio**: Suficiente para reportes CSV
- **Acceso**: Lectura a todas las unidades objetivo

## 🌐 Integración CO•RA

Estos scripts se integran con:
- **PLAN_EMERGENCIA.md**: Flujo de rescate prioritario
- **Scripts Python**: Inventarios y metadatos
- **Respaldo seguro**: Protección de información sensible

## 📈 Personalización

### Unidades Críticas ENTE56
```powershell
$UnidadesCriticas = @('C','D','G','H','I')
$UmbralEmergencia = 5  # GB
```

### Programación Personalizada
```powershell
# Diario a las 8:00 AM
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"

# Cada 3 días
$trigger = New-ScheduledTaskTrigger -Once -At "09:00" -RepetitionInterval (New-TimeSpan -Days 3)
```

---

*Herramientas de auditoría para el ecosistema CO•RA* 🛡️