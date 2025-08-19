#!/usr/bin/env python3
"""
Script de ejecución rápida para el Generador de Videos CO-RA
Interfaz simplificada para usuarios
"""

import sys
import os
from autopilot_oficial_video import autopilot_video_generator

def main():
    print("🎬 GENERADOR AUTOMÁTICO DE VIDEOS CO-RA")
    print("=" * 50)
    
    # Verificar configuración
    if not os.path.exists('.env'):
        print("⚠️  Archivo .env no encontrado")
        print("📋 Copia config/.env.example como .env y configura tu OPENAI_API_KEY")
        return
    
    # Obtener tema del usuario
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print("💡 Ejemplos de temas:")
        print("   - Impacto del cambio climático en México 2025")
        print("   - Avances en inteligencia artificial educativa")
        print("   - Políticas de inclusión digital en América Latina")
        print("   - Estadísticas de educación superior en México")
        print()
        topic = input("🎯 Ingresa el tema para tu video: ").strip()
    
    if not topic:
        print("❌ Tema requerido")
        return
    
    print(f"\n🚀 Generando video sobre: '{topic}'")
    print("⏱️  Tiempo estimado: 5-10 minutos")
    print()
    
    # Ejecutar generador
    success = autopilot_video_generator(topic)
    
    if success:
        print("\n🎉 ¡Video generado exitosamente!")
        print("📁 Revisa la carpeta 'output' para ver los resultados")
    else:
        print("\n❌ Error en la generación del video")
        print("🔧 Revisa la configuración y conexión a internet")

if __name__ == "__main__":
    main()