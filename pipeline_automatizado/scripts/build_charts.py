#!/usr/bin/env python3
"""
Generador de gráficos para videos - Pipeline CO-RA
Convierte CSV en gráficos PNG optimizados para video vertical
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import pathlib
from matplotlib import rcParams

def generate_salary_chart(csv_path, output_dir):
    """Genera gráfico de salarios optimizado para video vertical"""
    
    # Configuración para video
    rcParams['font.size'] = 16
    rcParams['font.weight'] = 'bold'
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Leer datos
    df = pd.read_csv(csv_path)
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Crear gráfico vertical
    fig, ax = plt.subplots(figsize=(8, 12))
    
    # Ordenar por salario y crear gráfico horizontal
    df_sorted = df.sort_values('salario', ascending=True)
    bars = ax.barh(df_sorted['puesto'], df_sorted['salario'], 
                   color='#0ea5e9', alpha=0.8, edgecolor='white', linewidth=2)
    
    # Personalización
    ax.set_xlabel('Salario (MXN mensuales)', fontsize=18, fontweight='bold')
    ax.set_ylabel('')
    ax.set_title('Comparativa de Sueldos - Morelos', 
                 fontsize=22, fontweight='bold', pad=20)
    
    # Formato de números
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Añadir valores en las barras
    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(df_sorted['salario']) * 0.01, bar.get_y() + bar.get_height()/2,
                f'${width:,.0f}', ha='left', va='center', fontweight='bold')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Guardar con alta resolución
    chart_path = output_path / 'chart_salarios.png'
    fig.savefig(chart_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    plt.close()
    print(f"Gráfico generado: {chart_path}")
    return str(chart_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python build_charts.py <csv_file> <output_dir>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    generate_salary_chart(csv_file, output_dir)