# 🔧 Esquema de Integración - Sistema CO•RA

## 📋 API de Integración para Programas Externos

### 🎯 **Flujo Completo de Ejecución**

```json
{
  "workflow": {
    "name": "CO-RA Storage Analysis",
    "version": "1.0",
    "steps": [
      {
        "id": "setup",
        "name": "Configuración Inicial",
        "type": "system",
        "commands": [
          "powershell -Command \"Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force\"",
          "mkdir \"%USERPROFILE%\\Desktop\\StorageReports\" -Force"
        ]
      },
      {
        "id": "scan",
        "name": "Escaneo Maestro",
        "type": "analysis",
        "command": "powershell -ExecutionPolicy Bypass -File \"{script_path}\\Escaneo-Maestro.ps1\" -IgnorarOcultas",
        "timeout": 600,
        "output_dir": "%USERPROFILE%\\Desktop\\StorageReports"
      },
      {
        "id": "process",
        "name": "Procesamiento de Resultados",
        "type": "data",
        "inputs": [
          "auditoria_{timestamp}.csv",
          "alertas_{timestamp}.csv", 
          "proyectos_{timestamp}.csv"
        ]
      }
    ]
  }
}
```

## 🔌 **Interfaces de Integración**

### **1. Línea de Comandos**
```bash
# Ejecución básica
powershell -ExecutionPolicy Bypass -File "Escaneo-Maestro.ps1"

# Con parámetros personalizados
powershell -ExecutionPolicy Bypass -File "Escaneo-Maestro.ps1" -Drives C,D,G,H,I -ThresholdGB 5 -OutputDir "C:\Reports"

# Modo silencioso (sin output visual)
powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File "Escaneo-Maestro.ps1" -IgnorarOcultas
```

### **2. Códigos de Salida**
```
0  = Éxito, sin alertas
1  = Error de ejecución
2  = Éxito, con alertas críticas
3  = Error de permisos
4  = Error de acceso a unidades
```

### **3. Estructura de Salida JSON**
```json
{
  "execution": {
    "timestamp": "2024-01-15T14:30:22",
    "status": "completed",
    "exit_code": 2,
    "duration_seconds": 347
  },
  "summary": {
    "drives_analyzed": 5,
    "critical_alerts": 2,
    "projects_found": 47,
    "total_recycle_bin_gb": 10.56
  },
  "files_generated": [
    "auditoria_20240115_143022.csv",
    "alertas_20240115_143022.csv",
    "proyectos_20240115_143022.csv"
  ]
}
```

## 🔄 **Integración con Diferentes Lenguajes**

### **Python Integration**
```python
import subprocess
import json
import os
from datetime import datetime

class CORAIntegration:
    def __init__(self, script_path):
        self.script_path = script_path
        self.output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "StorageReports")
    
    def execute_scan(self, drives=None, threshold_gb=10):
        cmd = [
            "powershell", "-ExecutionPolicy", "Bypass", "-File", 
            os.path.join(self.script_path, "Escaneo-Maestro.ps1"),
            "-IgnorarOcultas"
        ]
        
        if drives:
            cmd.extend(["-Drives", ",".join(drives)])
        if threshold_gb:
            cmd.extend(["-ThresholdGB", str(threshold_gb)])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def get_latest_reports(self):
        files = os.listdir(self.output_dir)
        reports = {
            "auditoria": None,
            "alertas": None, 
            "proyectos": None
        }
        
        for file in files:
            if file.startswith("auditoria_"):
                reports["auditoria"] = os.path.join(self.output_dir, file)
            elif file.startswith("alertas_"):
                reports["alertas"] = os.path.join(self.output_dir, file)
            elif file.startswith("proyectos_"):
                reports["proyectos"] = os.path.join(self.output_dir, file)
                
        return reports

# Uso
cora = CORAIntegration("F:\\CO-RA_Ecosistema_Cognitivo_Inclusivo-main\\respaldo_ente56\\herramientas_windows")
result = cora.execute_scan(drives=["C", "D", "G", "H", "I"])
reports = cora.get_latest_reports()
```

### **C# Integration**
```csharp
using System;
using System.Diagnostics;
using System.IO;

public class CORAIntegration
{
    private string scriptPath;
    private string outputDir;
    
    public CORAIntegration(string scriptPath)
    {
        this.scriptPath = scriptPath;
        this.outputDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "StorageReports");
    }
    
    public ProcessResult ExecuteScan(string[] drives = null, int thresholdGB = 10)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = "powershell",
            Arguments = $"-ExecutionPolicy Bypass -File \"{Path.Combine(scriptPath, "Escaneo-Maestro.ps1")}\" -IgnorarOcultas",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };
        
        if (drives != null)
            startInfo.Arguments += $" -Drives {string.Join(",", drives)}";
            
        startInfo.Arguments += $" -ThresholdGB {thresholdGB}";
        
        using (var process = Process.Start(startInfo))
        {
            process.WaitForExit();
            return new ProcessResult
            {
                ExitCode = process.ExitCode,
                Output = process.StandardOutput.ReadToEnd(),
                Error = process.StandardError.ReadToEnd()
            };
        }
    }
}
```

### **Node.js Integration**
```javascript
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

class CORAIntegration {
    constructor(scriptPath) {
        this.scriptPath = scriptPath;
        this.outputDir = path.join(os.homedir(), 'Desktop', 'StorageReports');
    }
    
    async executeScan(options = {}) {
        const { drives = ['C','D','G','H','I'], thresholdGB = 10 } = options;
        
        const args = [
            '-ExecutionPolicy', 'Bypass',
            '-File', path.join(this.scriptPath, 'Escaneo-Maestro.ps1'),
            '-IgnorarOcultas',
            '-Drives', drives.join(','),
            '-ThresholdGB', thresholdGB.toString()
        ];
        
        return new Promise((resolve, reject) => {
            const process = spawn('powershell', args);
            let stdout = '';
            let stderr = '';
            
            process.stdout.on('data', (data) => stdout += data);
            process.stderr.on('data', (data) => stderr += data);
            
            process.on('close', (code) => {
                resolve({
                    exitCode: code,
                    stdout,
                    stderr,
                    reports: this.getLatestReports()
                });
            });
        });
    }
    
    getLatestReports() {
        const files = fs.readdirSync(this.outputDir);
        return {
            auditoria: files.find(f => f.startsWith('auditoria_')),
            alertas: files.find(f => f.startsWith('alertas_')),
            proyectos: files.find(f => f.startsWith('proyectos_'))
        };
    }
}

// Uso
const cora = new CORAIntegration('F:\\CO-RA_Ecosistema_Cognitivo_Inclusivo-main\\respaldo_ente56\\herramientas_windows');
cora.executeScan({ drives: ['C','D','G','H','I'], thresholdGB: 5 })
    .then(result => console.log(result));
```

## 📊 **Formato de Datos de Salida**

### **CSV Structure**
```csv
# auditoria_YYYYMMDD_HHMMSS.csv
Drive,TotalBytes,FreeBytes,UsedBytes,PercentFree,RecycleBinB,TotalText,FreeText,UsedText,RecycleBinText

# alertas_YYYYMMDD_HHMMSS.csv  
Drive,FreeBytes,PercentFree

# proyectos_YYYYMMDD_HHMMSS.csv
Drive,Carpeta,Nombre,UltimaMod,Tamaño
```

### **JSON Conversion Schema**
```json
{
  "auditoria": [
    {
      "drive": "C:",
      "total_bytes": 500107862016,
      "free_bytes": 48563445760,
      "used_bytes": 451544416256,
      "percent_free": 9.71,
      "recycle_bin_bytes": 2516582400,
      "total_text": "465.76 GB",
      "free_text": "45.23 GB",
      "used_text": "420.53 GB",
      "recycle_bin_text": "2.34 GB"
    }
  ],
  "alertas": [
    {
      "drive": "C:",
      "free_bytes": 48563445760,
      "percent_free": 9.71,
      "criticality": "high"
    }
  ],
  "proyectos": [
    {
      "drive": "D",
      "path": "D:\\Documentos\\proyecto-tesis-final",
      "name": "proyecto-tesis-final",
      "last_modified": "2024-01-15T14:30:22",
      "size": "2.34 GB",
      "priority": "critical"
    }
  ]
}
```

## 🔧 **Parámetros de Configuración**

### **Entrada (Input Parameters)**
```json
{
  "drives": ["C", "D", "G", "H", "I"],
  "threshold_gb": 10,
  "keywords": ["proyecto", "tesis", "UMED", "github"],
  "output_dir": "C:\\Reports",
  "ignore_hidden": true,
  "timeout_seconds": 600
}
```

### **Salida (Output Parameters)**
```json
{
  "status": "completed|failed|timeout",
  "exit_code": 0,
  "execution_time": 347,
  "drives_scanned": 5,
  "alerts_count": 2,
  "projects_found": 47,
  "reports_generated": 3,
  "output_files": ["auditoria.csv", "alertas.csv", "proyectos.csv"]
}
```

## 🚀 **Ejemplo de Integración Completa**

### **Batch Script para Automatización**
```batch
@echo off
setlocal enabledelayedexpansion

set SCRIPT_DIR=F:\CO-RA_Ecosistema_Cognitivo_Inclusivo-main\respaldo_ente56\herramientas_windows
set OUTPUT_DIR=%USERPROFILE%\Desktop\StorageReports
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

echo [%TIMESTAMP%] Iniciando escaneo CO-RA...

powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%\Escaneo-Maestro.ps1" -IgnorarOcultas

if %ERRORLEVEL% EQU 0 (
    echo [%TIMESTAMP%] Escaneo completado exitosamente
) else if %ERRORLEVEL% EQU 2 (
    echo [%TIMESTAMP%] Escaneo completado con alertas criticas
) else (
    echo [%TIMESTAMP%] Error en el escaneo: %ERRORLEVEL%
)

echo Reportes generados en: %OUTPUT_DIR%
```

## 📋 **Checklist de Integración**

### **Pre-requisitos**
- [ ] PowerShell 5.1+ instalado
- [ ] Permisos de administrador disponibles
- [ ] Acceso de lectura a todas las unidades objetivo
- [ ] Espacio suficiente para reportes (< 10 MB)

### **Validaciones**
- [ ] Verificar códigos de salida
- [ ] Confirmar generación de 3 archivos CSV
- [ ] Validar formato de timestamps
- [ ] Comprobar permisos de escritura en output_dir

### **Manejo de Errores**
- [ ] Timeout de ejecución (10 minutos máximo)
- [ ] Unidades no accesibles
- [ ] Permisos insuficientes
- [ ] Espacio insuficiente para reportes

---

*Esquema completo para integración con cualquier sistema externo* 🔧