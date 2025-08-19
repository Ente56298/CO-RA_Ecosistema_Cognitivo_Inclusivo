# 📊 Guía de Interpretación - Escaneo Maestro CO•RA

## 🎯 Cómo Leer y Priorizar los 3 Reportes CSV

### 📋 **1. auditoria_YYYYMMDD_HHMMSS.csv**

#### Columnas Clave:
- **`Drive`**: Letra de unidad (C:, D:, G:, etc.)
- **`PercentFree`**: % de espacio libre ⚠️ **Crítico si < 10%**
- **`FreeText`**: Espacio libre en GB/TB
- **`RecycleBinText`**: Tamaño de papelera 🗑️

#### Interpretación Rápida:
```
PercentFree < 5%   → 🚨 EMERGENCIA - Actuar YA
PercentFree < 10%  → ⚠️  ALERTA - Planificar acción
PercentFree < 20%  → 💛 PRECAUCIÓN - Monitorear
PercentFree > 20%  → ✅ OK
```

#### Ejemplo de Lectura:
```csv
Drive,PercentFree,FreeText,RecycleBinText
D:,0.91,8.45 GB,5.67 GB
```
**Interpretación**: 
- 🚨 **CRÍTICO**: Solo 8.45 GB libres (0.91%)
- 🗑️ **OPORTUNIDAD**: 5.67 GB en papelera para evaluar

---

### ⚠️ **2. alertas_YYYYMMDD_HHMMSS.csv**

#### Priorización por Criticidad:
1. **PercentFree < 1%** → Acción inmediata (horas)
2. **PercentFree < 5%** → Acción urgente (1-2 días)  
3. **PercentFree < 10%** → Acción programada (1 semana)

#### Plan de Acción por Unidad:
```
C: (Sistema) → Limpiar temporales, mover datos usuario
D: (Datos)   → Migrar archivos grandes, evaluar papelera
G,H,I: (Ext) → Mover a unidades con más espacio
```

---

### 🔍 **3. proyectos_YYYYMMDD_HHMMSS.csv**

#### Columnas de Decisión:
- **`Drive`**: ¿Está en unidad crítica?
- **`UltimaMod`**: ¿Qué tan reciente es?
- **`Tamaño`**: ¿Vale la pena mover?
- **`Nombre`**: ¿Qué tan importante es?

#### Matriz de Prioridades:

| Criticidad Unidad | Fecha Reciente | Tamaño Grande | Acción |
|-------------------|----------------|---------------|---------|
| 🚨 Crítica | ✅ Sí | ✅ Sí | **RESCATAR YA** |
| 🚨 Crítica | ✅ Sí | ❌ No | **RESCATAR** |
| 🚨 Crítica | ❌ No | ✅ Sí | **MIGRAR** |
| ⚠️ Alerta | ✅ Sí | ✅ Sí | **PLANIFICAR** |
| ✅ OK | - | - | **MANTENER** |

---

## 🎯 **Estrategia de Reorganización en 4 Fases**

### **FASE 1: RESCATE INMEDIATO** (Hoy)
```powershell
# Identificar proyectos críticos
# Filtro: Drive en alerta + UltimaMod reciente + Tamaño > 100MB
```

**Criterios**:
- Unidad con < 5% libre
- Modificado en últimos 30 días  
- Tamaño > 100 MB
- Nombres: "tesis", "proyecto", "UMED", "final"

**Acción**: Copiar a unidad segura (M:, nube, externo)

### **FASE 2: EVALUACIÓN DE PAPELERAS** (Hoy)
```powershell
# Revisar papeleras grandes antes de vaciar
# Filtro: RecycleBinText > 1 GB
```

**Proceso**:
1. Abrir papelera de unidades críticas
2. Buscar archivos importantes por fecha/nombre
3. Restaurar lo necesario
4. Vaciar el resto

### **FASE 3: MIGRACIÓN PLANIFICADA** (1-3 días)
```powershell
# Mover archivos grandes antiguos
# Filtro: Tamaño > 500MB + UltimaMod > 60 días
```

**Criterios**:
- Archivos > 500 MB
- No modificados en 60+ días
- En unidades con < 20% libre

### **FASE 4: OPTIMIZACIÓN** (1 semana)
```powershell
# Reorganizar estructura general
# Comprimir, archivar, limpiar duplicados
```

---

## 📈 **Ejemplo Práctico de Interpretación**

### Datos del CSV:
```csv
# auditoria.csv
Drive,PercentFree,FreeText,RecycleBinText
D:,0.91,8.45 GB,5.67 GB
G:,8.41,156.78 GB,890.45 MB

# proyectos.csv  
Drive,Nombre,UltimaMod,Tamaño
D,proyecto-tesis-final,2024-01-15,2.34 GB
D,UMED-trabajos,2024-01-12,1.56 GB
G,repos-antiguos,2023-08-20,3.45 GB
```

### Interpretación y Acciones:

#### 🚨 **CRÍTICO - Unidad D:**
- **Estado**: 0.91% libre (8.45 GB) - EMERGENCIA
- **Papelera**: 5.67 GB - Revisar contenido YA
- **Proyectos críticos**:
  - `proyecto-tesis-final` (2.34 GB, reciente) → **RESCATAR HOY**
  - `UMED-trabajos` (1.56 GB, reciente) → **RESCATAR HOY**

#### ⚠️ **ALERTA - Unidad G:**
- **Estado**: 8.41% libre (156.78 GB) - Planificar
- **Proyectos**:
  - `repos-antiguos` (3.45 GB, 5 meses) → **MIGRAR a M:**

#### 📋 **Plan de Acción Inmediato**:
1. **Ahora**: Copiar `proyecto-tesis-final` y `UMED-trabajos` de D: a M:
2. **Hoy**: Revisar papelera de D: (5.67 GB)
3. **Esta semana**: Mover `repos-antiguos` de G: a M:

---

## 🛠️ **Comandos Rápidos de Rescate**

### Rescate Inmediato:
```powershell
# Crear carpeta de rescate
mkdir "M:\Rescate_Emergencia_$(Get-Date -Format 'yyyyMMdd')"

# Copiar proyectos críticos
robocopy "D:\ruta\proyecto-tesis-final" "M:\Rescate_Emergencia_20240115\proyecto-tesis-final" /E /COPY:DAT
```

### Evaluación de Papelera:
```powershell
# Ver contenido de papelera por tamaño
Get-ChildItem "D:\$Recycle.Bin" -Recurse -Force | Sort-Object Length -Descending | Select-Object -First 20
```

---

*Con esta guía puedes convertir los números del CSV en acciones concretas y estratégicas* 🎯