#!/usr/bin/env python3
"""
Organizador de respaldo seguro ENTE56
Clasifica y organiza documentos por categorías
"""

import os
import json
import shutil
from pathlib import Path
import argparse

class OrganizadorRespaldo:
    def __init__(self):
        self.categorias = {
            "academico": {
                "descripcion": "Documentos académicos y educativos",
                "extensiones_seguras": [".pdf", ".docx", ".pptx", ".txt", ".md"],
                "carpetas_origen": ["UMED", "recursos", "tareas"]
            },
            "tecnico": {
                "descripcion": "Código, configuraciones y documentación técnica", 
                "extensiones_seguras": [".py", ".js", ".html", ".css", ".md", ".json", ".yml"],
                "carpetas_origen": ["proyectos", "scripts", "config"]
            },
            "profesional": {
                "descripcion": "Documentos de trabajo públicos",
                "extensiones_seguras": [".pdf", ".docx", ".pptx", ".md"],
                "carpetas_origen": ["doc importantes", "presentaciones"]
            }
        }
    
    def es_archivo_seguro(self, archivo, categoria):
        """Verifica si un archivo es seguro para incluir en el repo"""
        extension = Path(archivo).suffix.lower()
        extensiones_permitidas = self.categorias[categoria]["extensiones_seguras"]
        
        # Verificar extensión
        if extension not in extensiones_permitidas:
            return False
            
        # Verificar contenido sensible en nombre
        nombre_lower = archivo.lower()
        palabras_sensibles = [
            "curp", "rfc", "nomina", "sueldo", "banco", "tarjeta",
            "credencial", "password", "clave", "personal", "privado"
        ]
        
        return not any(palabra in nombre_lower for palabra in palabras_sensibles)
    
    def organizar_por_categoria(self, categoria, ruta_origen):
        """Organiza archivos por categoría específica"""
        if categoria not in self.categorias:
            print(f"Categoría no válida: {categoria}")
            return
            
        carpeta_destino = f"documentos_publicos/{categoria}"
        os.makedirs(carpeta_destino, exist_ok=True)
        
        archivos_copiados = []
        archivos_omitidos = []
        
        for root, dirs, files in os.walk(ruta_origen):
            for archivo in files:
                ruta_origen_archivo = os.path.join(root, archivo)
                
                if self.es_archivo_seguro(archivo, categoria):
                    # Crear estructura de carpetas en destino
                    ruta_relativa = os.path.relpath(root, ruta_origen)
                    carpeta_destino_archivo = os.path.join(carpeta_destino, ruta_relativa)
                    os.makedirs(carpeta_destino_archivo, exist_ok=True)
                    
                    # Copiar archivo
                    ruta_destino_archivo = os.path.join(carpeta_destino_archivo, archivo)
                    shutil.copy2(ruta_origen_archivo, ruta_destino_archivo)
                    
                    archivos_copiados.append({
                        "archivo": archivo,
                        "origen": ruta_origen_archivo,
                        "destino": ruta_destino_archivo
                    })
                else:
                    archivos_omitidos.append({
                        "archivo": archivo,
                        "razon": "Archivo sensible o extensión no permitida"
                    })
        
        # Generar reporte de organización
        reporte = {
            "categoria": categoria,
            "fecha_organizacion": Path().cwd(),
            "archivos_copiados": len(archivos_copiados),
            "archivos_omitidos": len(archivos_omitidos),
            "detalles_copiados": archivos_copiados,
            "detalles_omitidos": archivos_omitidos
        }
        
        with open(f"metadatos/organizacion_{categoria}.json", 'w') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
            
        return reporte
    
    def generar_indice_general(self):
        """Genera índice general de todos los documentos organizados"""
        indice = {
            "generado": str(Path().cwd()),
            "categorias": {}
        }
        
        for categoria, info in self.categorias.items():
            carpeta = f"documentos_publicos/{categoria}"
            if os.path.exists(carpeta):
                archivos = []
                for root, dirs, files in os.walk(carpeta):
                    for archivo in files:
                        archivos.append({
                            "nombre": archivo,
                            "ruta": os.path.relpath(os.path.join(root, archivo)),
                            "tamaño_kb": round(os.path.getsize(os.path.join(root, archivo)) / 1024, 2)
                        })
                
                indice["categorias"][categoria] = {
                    "descripcion": info["descripcion"],
                    "total_archivos": len(archivos),
                    "archivos": archivos
                }
        
        with open("metadatos/indice_general.json", 'w') as f:
            json.dump(indice, f, indent=2, ensure_ascii=False)
            
        return indice

def main():
    parser = argparse.ArgumentParser(description='Organizar respaldo por categorías')
    parser.add_argument('--categoria', required=True, 
                       choices=['academico', 'tecnico', 'profesional'],
                       help='Categoría a organizar')
    parser.add_argument('--origen', required=True, help='Ruta de origen de los archivos')
    
    args = parser.parse_args()
    
    organizador = OrganizadorRespaldo()
    
    print(f"Organizando categoría: {args.categoria}")
    print(f"Desde: {args.origen}")
    
    reporte = organizador.organizar_por_categoria(args.categoria, args.origen)
    
    if reporte:
        print(f"Archivos copiados: {reporte['archivos_copiados']}")
        print(f"Archivos omitidos: {reporte['archivos_omitidos']}")
        
        # Generar índice general actualizado
        organizador.generar_indice_general()
        print("Índice general actualizado")

if __name__ == "__main__":
    main()