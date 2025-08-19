#!/usr/bin/env python3
"""
INVENTARIO RÁPIDO DE EMERGENCIA
Genera listado completo de archivos rescatados
"""

import os
import json
from datetime import datetime
from pathlib import Path
import sys

def inventario_rapido(ruta_base):
    """Genera inventario completo de archivos"""
    inventario = {
        "fecha_inventario": datetime.now().isoformat(),
        "ruta_base": str(ruta_base),
        "total_archivos": 0,
        "total_size_mb": 0,
        "carpetas": {}
    }
    
    if not os.path.exists(ruta_base):
        print(f"❌ Ruta no existe: {ruta_base}")
        return None
    
    print(f"📋 Inventariando: {ruta_base}")
    
    for root, dirs, files in os.walk(ruta_base):
        carpeta_rel = os.path.relpath(root, ruta_base)
        
        archivos_carpeta = []
        size_carpeta = 0
        
        for archivo in files:
            ruta_archivo = os.path.join(root, archivo)
            try:
                stat = os.stat(ruta_archivo)
                size_mb = stat.st_size / (1024 * 1024)
                
                archivos_carpeta.append({
                    "nombre": archivo,
                    "size_mb": round(size_mb, 2),
                    "fecha_mod": datetime.fromtimestamp(stat.st_mtime).isoformat()[:19],
                    "extension": Path(archivo).suffix.lower()
                })
                
                size_carpeta += size_mb
                inventario["total_archivos"] += 1
                inventario["total_size_mb"] += size_mb
                
            except Exception as e:
                print(f"⚠️  Error con {archivo}: {e}")
        
        if archivos_carpeta:
            inventario["carpetas"][carpeta_rel] = {
                "archivos": len(archivos_carpeta),
                "size_mb": round(size_carpeta, 2),
                "contenido": archivos_carpeta
            }
    
    # Guardar inventario
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_inventario = f"metadatos/inventario_emergencia_{timestamp}.json"
    
    os.makedirs("metadatos", exist_ok=True)
    with open(archivo_inventario, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=2, ensure_ascii=False)
    
    return inventario, archivo_inventario

def resumen_rapido(inventario):
    """Muestra resumen ejecutivo"""
    print("\n" + "="*50)
    print("📊 RESUMEN DE RESCATE")
    print("="*50)
    print(f"📁 Total archivos: {inventario['total_archivos']}")
    print(f"💾 Tamaño total: {inventario['total_size_mb']:.1f} MB")
    print(f"📂 Carpetas: {len(inventario['carpetas'])}")
    
    print("\n🔝 TOP CARPETAS:")
    carpetas_ordenadas = sorted(
        inventario['carpetas'].items(), 
        key=lambda x: x[1]['size_mb'], 
        reverse=True
    )[:5]
    
    for carpeta, info in carpetas_ordenadas:
        print(f"  📂 {carpeta}: {info['archivos']} archivos, {info['size_mb']:.1f} MB")
    
    print("\n📋 Inventario guardado en: metadatos/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 inventario_rapido.py /ruta/respaldo_local")
        sys.exit(1)
    
    ruta = sys.argv[1]
    resultado = inventario_rapido(ruta)
    
    if resultado:
        inventario, archivo = resultado
        resumen_rapido(inventario)
        print(f"\n✅ Inventario completo: {archivo}")
    else:
        print("❌ No se pudo generar el inventario")