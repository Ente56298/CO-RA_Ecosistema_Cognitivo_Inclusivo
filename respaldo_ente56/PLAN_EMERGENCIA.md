# 🚨 PLAN DE EMERGENCIA - Rescate ENTE56

## ⏰ ACCIÓN INMEDIATA (HOY)

### 1️⃣ OneDrive UnADM - PRIORIDAD MÁXIMA
```bash
# Desde tu móvil/PC con sesión activa:
# 1. Ir a OneDrive web
# 2. Seleccionar TODO → Descargar
# 3. Guardar en: /respaldo_local/onedrive_unadm/
```

### 2️⃣ Correo Outlook ENTE56
```bash
# Filtros a aplicar:
# - "Tiene: adjuntos" 
# - Por carpetas: UMED, doc importantes, facturas, nomina
# - Descargar adjuntos por lotes
# - Guardar en: /respaldo_local/correo_ente56/
```

### 3️⃣ Discos Dañados - RECUPERACIÓN
```bash
# NO usar los discos hasta recuperar
# Conectar a otra PC
# Usar: Recuva, TestDisk, PhotoRec
# Guardar recuperado en: /respaldo_local/recuperados/
```

---

## 📋 CHECKLIST DE RESCATE

- [ ] OneDrive descargado completo
- [ ] Correos con adjuntos extraídos  
- [ ] Archivos de discos recuperados
- [ ] To-Do/Notas exportadas
- [ ] Inventario generado con script
- [ ] Respaldo en nube personal
- [ ] Commit verificado en repo

---

## 🔧 HERRAMIENTAS LISTAS

### 🐍 Python (Linux/Mac):
```bash
# Generar inventario rápido
python3 scripts/inventario_rapido.py /ruta/respaldo_local

# Clasificar por urgencia
python3 scripts/clasificar_urgencia.py
```

### 🪟 PowerShell (Windows):
```powershell
# Auditoría completa de discos
.\herramientas_windows\Auditoria-Almacenamiento.ps1 -Drives C,D,G,H,I -ThresholdGB 10

# Programar monitoreo automático
.\herramientas_windows\Programar-Auditoria.ps1

# Migrar archivos grandes (SOLO después del rescate)
.\herramientas_windows\Mover-Archivos-Grandes.ps1 -DoIt
```

---

## 📂 ESTRUCTURA DE RESPALDO LOCAL

```
/respaldo_local/
├── onedrive_unadm/     # Descarga completa OneDrive
├── correo_ente56/      # Adjuntos por carpetas
├── recuperados/        # Archivos de discos dañados
├── exportados/         # To-Do, notas, listas
└── inventarios/        # Listados generados
```

---

## 🛡️ REGLAS DE SEGURIDAD

✅ **Subir al repo**: Solo inventarios y metadatos
❌ **NO subir**: Archivos originales, datos personales
🔄 **Redundancia**: Local + Nube personal + Disco externo

---

*Tiempo estimado de rescate: 2-4 horas*
*Prioridad: OneDrive > Correo > Recuperación*