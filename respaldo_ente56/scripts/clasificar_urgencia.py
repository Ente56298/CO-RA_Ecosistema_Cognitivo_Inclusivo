#!/usr/bin/env python3
"""
CLASIFICADOR DE URGENCIA
Identifica archivos críticos que necesitan respaldo inmediato
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class ClasificadorUrgencia:
    def __init__(self):
        self.categorias_criticas = {
            "CRITICO": {
                "palabras": ["tesis", "proyecto", "final", "entrega", "importante"],
                "extensiones": [".docx", ".pdf", ".pptx"],
                "descripcion": "Documentos académicos/profesionales críticos"
            },
            "FINANCIERO": {
                "palabras": ["factura", "nomina", "banco", "pago", "recibo"],
                "extensiones": [".pdf", ".xlsx"],
                "descripcion": "Documentos financieros y fiscales"
            },
            "CODIGO": {
                "palabras": ["proyecto", "script", "codigo"],
                "extensiones": [".py", ".js", ".html", ".css", ".json"],
                "descripcion": "Código y desarrollo"
            },
            "PERSONAL": {
                "palabras": ["curp", "rfc", "credencial", "certificado"],
                "extensiones": [".pdf", ".jpg", ".png"],
                "descripcion": "Documentos personales oficiales"
            }
        }
    
    def clasificar_archivo(self, nombre_archivo, ruta_archivo):
        """Clasifica un archivo por urgencia"""
        nombre_lower = nombre_archivo.lower()
        extension = Path(nombre_archivo).suffix.lower()
        
        # Verificar si es reciente (últimos 30 días)
        try:
            stat = os.stat(ruta_archivo)
            fecha_mod = datetime.fromtimestamp(stat.st_mtime)
            es_reciente = (datetime.now() - fecha_mod).days <= 30
        except:
            es_reciente = False
        
        clasificaciones = []
        
        for categoria, criterios in self.categorias_criticas.items():
            puntos = 0
            
            # Verificar palabras clave
            for palabra in criterios["palabras"]:
                if palabra in nombre_lower:
                    puntos += 2
            
            # Verificar extensión
            if extension in criterios["extensiones"]:
                puntos += 1
            
            # Bonus por archivo reciente
            if es_reciente:
                puntos += 1
            
            if puntos >= 2:
                clasificaciones.append({
                    "categoria": categoria,
                    "puntos": puntos,
                    "descripcion": criterios["descripcion"]
                })
        
        return clasificaciones
    
    def procesar_inventario(self, archivo_inventario):
        """Procesa inventario existente y clasifica por urgencia"""
        if not os.path.exists(archivo_inventario):
            print(f"❌ Inventario no encontrado: {archivo_inventario}")
            return None
        
        with open(archivo_inventario, 'r', encoding='utf-8') as f:
            inventario = json.load(f)
        
        archivos_criticos = {
            "CRITICO": [],
            "FINANCIERO": [],
            "CODIGO": [],
            "PERSONAL": []
        }
        
        total_procesados = 0
        
        for carpeta, info in inventario["carpetas"].items():
            for archivo_info in info["contenido"]:
                nombre = archivo_info["nombre"]
                ruta_simulada = f"{inventario['ruta_base']}/{carpeta}/{nombre}"
                
                clasificaciones = self.clasificar_archivo(nombre, ruta_simulada)
                
                if clasificaciones:
                    archivo_clasificado = {
                        "nombre": nombre,
                        "carpeta": carpeta,
                        "size_mb": archivo_info["size_mb"],
                        "fecha_mod": archivo_info["fecha_mod"],
                        "clasificaciones": clasificaciones
                    }
                    
                    # Añadir a la categoría con mayor puntuación
                    mejor_categoria = max(clasificaciones, key=lambda x: x["puntos"])
                    archivos_criticos[mejor_categoria["categoria"]].append(archivo_clasificado)
                
                total_procesados += 1
        
        # Generar reporte de urgencia
        reporte_urgencia = {
            "fecha_clasificacion": datetime.now().isoformat(),
            "total_archivos_procesados": total_procesados,
            "archivos_criticos": archivos_criticos,
            "resumen": {
                categoria: len(archivos) 
                for categoria, archivos in archivos_criticos.items()
            }
        }
        
        # Guardar reporte
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_reporte = f"metadatos/urgencia_{timestamp}.json"
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte_urgencia, f, indent=2, ensure_ascii=False)
        
        return reporte_urgencia, archivo_reporte
    
    def mostrar_resumen_urgencia(self, reporte):
        """Muestra resumen de archivos críticos"""
        print("\n" + "🚨"*20)
        print("🚨 CLASIFICACIÓN DE URGENCIA")
        print("🚨"*20)
        
        for categoria, archivos in reporte["archivos_criticos"].items():
            if archivos:
                print(f"\n🔴 {categoria} ({len(archivos)} archivos):")
                for archivo in archivos[:5]:  # Top 5
                    print(f"  📄 {archivo['nombre']} ({archivo['size_mb']} MB)")
                    print(f"     📂 {archivo['carpeta']}")
                if len(archivos) > 5:
                    print(f"     ... y {len(archivos) - 5} más")

if __name__ == "__main__":
    clasificador = ClasificadorUrgencia()
    
    # Buscar el inventario más reciente
    inventarios = [f for f in os.listdir("metadatos/") if f.startswith("inventario_emergencia_")]
    
    if not inventarios:
        print("❌ No se encontró inventario. Ejecuta primero: inventario_rapido.py")
        exit(1)
    
    inventario_reciente = sorted(inventarios)[-1]
    archivo_inventario = f"metadatos/{inventario_reciente}"
    
    print(f"📋 Procesando: {archivo_inventario}")
    
    resultado = clasificador.procesar_inventario(archivo_inventario)
    
    if resultado:
        reporte, archivo_reporte = resultado
        clasificador.mostrar_resumen_urgencia(reporte)
        print(f"\n✅ Reporte de urgencia: {archivo_reporte}")
    else:
        print("❌ Error al procesar inventario")