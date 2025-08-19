#!/usr/bin/env python3
"""
Generador de metadatos seguros para respaldo ENTE56
Extrae información de archivos sin exponer contenido sensible
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
import argparse

class GeneradorMetadatos:
    def __init__(self):
        self.categorias = {
            "UMED": "academico",
            "doc importantes": "profesional", 
            "facturas": "financiero",
            "nomina": "financiero",
            "proyectos": "tecnico",
            "recursos": "educativo"
        }
        
    def escanear_carpeta(self, ruta_carpeta):
        """Escanea carpeta y extrae metadatos seguros"""
        if not os.path.exists(ruta_carpeta):
            print(f"Carpeta no encontrada: {ruta_carpeta}")
            return []
            
        metadatos = []
        for root, dirs, files in os.walk(ruta_carpeta):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                stat = os.stat(ruta_completa)
                
                # Solo metadatos seguros
                metadata = {
                    "nombre_archivo": archivo,
                    "extension": Path(archivo).suffix.lower(),
                    "tamaño_kb": round(stat.st_size / 1024, 2),
                    "fecha_modificacion": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "ruta_relativa": os.path.relpath(ruta_completa, ruta_carpeta),
                    "es_sensible": self.detectar_sensible(archivo)
                }
                metadatos.append(metadata)
                
        return metadatos
    
    def detectar_sensible(self, nombre_archivo):
        """Detecta si un archivo puede contener información sensible"""
        sensibles = [
            "curp", "rfc", "nomina", "sueldo", "banco", 
            "tarjeta", "credencial", "password", "clave",
            "personal", "privado", "confidencial"
        ]
        
        nombre_lower = nombre_archivo.lower()
        return any(palabra in nombre_lower for palabra in sensibles)
    
    def generar_reporte_json(self, metadatos, carpeta_origen):
        """Genera reporte JSON de metadatos"""
        reporte = {
            "generado": datetime.now().isoformat(),
            "carpeta_origen": carpeta_origen,
            "total_archivos": len(metadatos),
            "archivos_sensibles": sum(1 for m in metadatos if m["es_sensible"]),
            "categoria": self.categorias.get(carpeta_origen, "general"),
            "metadatos": metadatos
        }
        
        nombre_archivo = f"metadatos_{carpeta_origen.replace(' ', '_')}.json"
        ruta_salida = f"metadatos/{nombre_archivo}"
        
        os.makedirs("metadatos", exist_ok=True)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
            
        return ruta_salida
    
    def generar_reporte_csv(self, metadatos, carpeta_origen):
        """Genera reporte CSV de metadatos"""
        nombre_archivo = f"metadatos_{carpeta_origen.replace(' ', '_')}.csv"
        ruta_salida = f"metadatos/{nombre_archivo}"
        
        os.makedirs("metadatos", exist_ok=True)
        with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
            if metadatos:
                writer = csv.DictWriter(f, fieldnames=metadatos[0].keys())
                writer.writeheader()
                writer.writerows(metadatos)
                
        return ruta_salida

def main():
    parser = argparse.ArgumentParser(description='Generar metadatos seguros de carpetas')
    parser.add_argument('--carpeta', required=True, help='Nombre de la carpeta a escanear')
    parser.add_argument('--ruta', help='Ruta completa (opcional)')
    parser.add_argument('--formato', choices=['json', 'csv', 'ambos'], default='ambos')
    
    args = parser.parse_args()
    
    generador = GeneradorMetadatos()
    ruta_carpeta = args.ruta or f"/ruta/local/respaldo/{args.carpeta}"
    
    print(f"Escaneando carpeta: {args.carpeta}")
    metadatos = generador.escanear_carpeta(ruta_carpeta)
    
    if not metadatos:
        print("No se encontraron archivos o la carpeta no existe")
        return
    
    if args.formato in ['json', 'ambos']:
        ruta_json = generador.generar_reporte_json(metadatos, args.carpeta)
        print(f"Reporte JSON generado: {ruta_json}")
    
    if args.formato in ['csv', 'ambos']:
        ruta_csv = generador.generar_reporte_csv(metadatos, args.carpeta)
        print(f"Reporte CSV generado: {ruta_csv}")
    
    sensibles = sum(1 for m in metadatos if m["es_sensible"])
    print(f"Total archivos: {len(metadatos)}")
    print(f"Archivos sensibles detectados: {sensibles}")

if __name__ == "__main__":
    main()