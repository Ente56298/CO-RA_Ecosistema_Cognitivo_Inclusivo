#!/usr/bin/env python3
"""
Conversor Markdown a SRT - Pipeline CO-RA
Genera subtítulos sincronizados desde guion en Markdown
"""

import sys
import textwrap
import re

def md_to_srt(md_file, output_file=None):
    """Convierte Markdown a formato SRT"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().splitlines()
    
    srt_content = []
    time_offset = 0
    subtitle_index = 1
    
    for line in lines:
        line = line.strip()
        
        # Saltar líneas vacías y headers
        if not line or line.startswith('#'):
            continue
        
        # Limpiar markdown básico
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Bold
        line = re.sub(r'\*(.*?)\*', r'\1', line)      # Italic
        line = re.sub(r'`(.*?)`', r'\1', line)        # Code
        
        # Calcular duración basada en longitud (10 caracteres por segundo)
        duration = max(2, int(len(line) / 10))
        
        # Formatear tiempo
        start_time = format_time(time_offset)
        end_time = format_time(time_offset + duration)
        
        # Crear entrada SRT
        srt_entry = f"{subtitle_index}\n{start_time} --> {end_time}\n{textwrap.fill(line, width=42)}\n"
        srt_content.append(srt_entry)
        
        time_offset += duration
        subtitle_index += 1
    
    # Guardar o imprimir
    srt_text = '\n'.join(srt_content)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt_text)
        print(f"SRT generado: {output_file}")
    else:
        print(srt_text)
    
    return srt_text

def format_time(seconds):
    """Convierte segundos a formato SRT (HH:MM:SS,mmm)"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d},000"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python md_to_srt.py <markdown_file> [output_file]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    md_to_srt(md_file, output_file)