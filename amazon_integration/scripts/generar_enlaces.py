#!/usr/bin/env python3
"""
Generador de enlaces de afiliado de Amazon
Integrado con el ecosistema CO-RA
"""

import os
import csv
import json
import re
from datetime import datetime
from pathlib import Path

class GeneradorEnlacesAmazon:
    def __init__(self):
        self.affiliate_tag = os.environ.get('AMAZON_AFFILIATE_TAG', 'cora-20')
        self.base_url = "https://www.amazon.com/dp/"
        
    def extraer_productos_templates(self, carpeta_templates):
        """Extrae referencias de productos de los templates"""
        productos = []
        
        if not os.path.exists(carpeta_templates):
            print(f"Carpeta templates no encontrada: {carpeta_templates}")
            return productos
            
        for archivo in Path(carpeta_templates).rglob("*"):
            if archivo.is_file() and archivo.suffix in ['.md', '.html', '.txt']:
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                        
                    # Buscar ASINs de Amazon (formato: B0XXXXXXXX)
                    asins = re.findall(r'B0[A-Z0-9]{8}', contenido)
                    
                    # Buscar URLs de Amazon
                    urls_amazon = re.findall(r'https://(?:www\.)?amazon\.com/[^\s]+', contenido)
                    
                    for asin in asins:
                        productos.append({
                            'asin': asin,
                            'archivo_origen': str(archivo),
                            'tipo': 'asin_directo'
                        })
                    
                    for url in urls_amazon:
                        asin_from_url = self.extraer_asin_de_url(url)
                        if asin_from_url:
                            productos.append({
                                'asin': asin_from_url,
                                'archivo_origen': str(archivo),
                                'tipo': 'url_amazon'
                            })
                            
                except Exception as e:
                    print(f"Error procesando {archivo}: {e}")
                    
        return productos
    
    def extraer_asin_de_url(self, url):
        """Extrae ASIN de una URL de Amazon"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def generar_enlace_afiliado(self, asin):
        """Genera enlace de afiliado para un ASIN"""
        return f"{self.base_url}{asin}?tag={self.affiliate_tag}"
    
    def procesar_productos(self, productos):
        """Procesa lista de productos y genera enlaces"""
        enlaces_generados = []
        
        for producto in productos:
            enlace_afiliado = self.generar_enlace_afiliado(producto['asin'])
            
            enlaces_generados.append({
                'asin': producto['asin'],
                'enlace_afiliado': enlace_afiliado,
                'archivo_origen': producto['archivo_origen'],
                'tipo': producto['tipo'],
                'fecha_generacion': datetime.now().isoformat(),
                'tag_afiliado': self.affiliate_tag
            })
            
        return enlaces_generados
    
    def guardar_enlaces_csv(self, enlaces, archivo_csv):
        """Guarda enlaces en archivo CSV"""
        os.makedirs(os.path.dirname(archivo_csv), exist_ok=True)
        
        fieldnames = ['asin', 'enlace_afiliado', 'archivo_origen', 'tipo', 'fecha_generacion', 'tag_afiliado']
        
        with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enlaces)
    
    def generar_reporte_json(self, enlaces, archivo_json):
        """Genera reporte JSON detallado"""
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'total_enlaces': len(enlaces),
            'tag_afiliado': self.affiliate_tag,
            'enlaces': enlaces,
            'estadisticas': {
                'por_tipo': {},
                'por_archivo': {}
            }
        }
        
        # Estadísticas por tipo
        for enlace in enlaces:
            tipo = enlace['tipo']
            reporte['estadisticas']['por_tipo'][tipo] = reporte['estadisticas']['por_tipo'].get(tipo, 0) + 1
            
            archivo = enlace['archivo_origen']
            reporte['estadisticas']['por_archivo'][archivo] = reporte['estadisticas']['por_archivo'].get(archivo, 0) + 1
        
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        return reporte

def main():
    generador = GeneradorEnlacesAmazon()
    
    # Carpetas de trabajo
    carpeta_templates = "amazon_integration/templates"
    archivo_csv = "amazon_integration/data/links.csv"
    archivo_json = "amazon_integration/data/reporte_enlaces.json"
    
    print("🔍 Escaneando templates...")
    productos = generador.extraer_productos_templates(carpeta_templates)
    
    if not productos:
        print("ℹ️  No se encontraron productos en templates")
        return
    
    print(f"📦 Encontrados {len(productos)} productos")
    
    # Generar enlaces
    enlaces = generador.procesar_productos(productos)
    
    # Guardar resultados
    generador.guardar_enlaces_csv(enlaces, archivo_csv)
    reporte = generador.generar_reporte_json(enlaces, archivo_json)
    
    print(f"✅ Enlaces guardados en: {archivo_csv}")
    print(f"📊 Reporte generado en: {archivo_json}")
    print(f"🔗 Total enlaces generados: {len(enlaces)}")
    
    # Mostrar resumen
    for tipo, cantidad in reporte['estadisticas']['por_tipo'].items():
        print(f"   {tipo}: {cantidad}")

if __name__ == "__main__":
    main()