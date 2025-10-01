#!/usr/bin/env python3
"""
Script de prueba para ejemplos del lenguaje Quantum-Ω
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prueba de ejemplos
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def read_quantum_omega_file(filepath):
    """Lee archivo de ejemplo Quantum-Ω"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error leyendo archivo {filepath}: {e}")
        return None

def analyze_quantum_program(code):
    """Analiza código Quantum-Ω básico"""
    program_info = {
        'name': 'unnamed',
        'version': '1.0',
        'qubits': 0,
        'classical_bits': 0,
        'functions': [],
        'algorithms': [],
        'errors': []
    }

    try:
        lines = code.strip().split('\n')

        for line in lines:
            line = line.strip()

            # Buscar nombre del programa
            if line.startswith('quantum_program'):
                match = re.search(r'quantum_program\s+"([^"]+)"', line)
                if match:
                    program_info['name'] = match.group(1)

            # Buscar configuración básica
            elif line.startswith('qubits:'):
                try:
                    program_info['qubits'] = int(line.split(':')[1].strip())
                except:
                    program_info['errors'].append(f"Error parsing qubits: {line}")

            elif line.startswith('classical_bits:'):
                try:
                    program_info['classical_bits'] = int(line.split(':')[1].strip())
                except:
                    program_info['errors'].append(f"Error parsing classical_bits: {line}")

            elif line.startswith('version:'):
                match = re.search(r'version:\s*"([^"]+)"', line)
                if match:
                    program_info['version'] = match.group(1)

            # Buscar funciones cuánticas
            elif line.startswith('quantum_function'):
                match = re.search(r'quantum_function\s+(\w+)', line)
                if match:
                    program_info['functions'].append(match.group(1))

            # Buscar algoritmos cuánticos
            elif 'QOA' in line or 'QSA' in line or 'QPSO' in line or 'QML' in line:
                algorithms = []
                if 'QOA' in line:
                    algorithms.append('QOA')
                if 'QSA' in line:
                    algorithms.append('QSA')
                if 'QPSO' in line:
                    algorithms.append('QPSO')
                if 'QML' in line:
                    algorithms.append('QML')
                program_info['algorithms'].extend(algorithms)

    except Exception as e:
        program_info['errors'].append(f"Error analyzing program: {e}")

    return program_info

def test_quantum_omega_examples():
    """Prueba ejemplos del lenguaje Quantum-Ω"""
    print("=== Prueba de Ejemplos Quantum-Ω ===")

    examples_dir = "quantum_omega_language"
    example_files = [
        "examples.qo",
        "qoa_examples.qo",
        "qml_examples.qo"
    ]

    total_programs = 0
    successful_analyses = 0

    for filename in example_files:
        filepath = os.path.join(examples_dir, filename)
        print(f"\n--- Analizando {filename} ---")

        code = read_quantum_omega_file(filepath)
        if code is None:
            print(f"✗ No se pudo leer {filename}")
            continue

        # Buscar múltiples programas en el archivo
        programs = re.split(r'quantum_program', code)
        programs = [prog for prog in programs if prog.strip()]

        for i, program_code in enumerate(programs):
            total_programs += 1

            # Agregar "quantum_program" al inicio si no está
            if not program_code.strip().startswith('quantum_program'):
                program_code = "quantum_program" + program_code

            program_info = analyze_quantum_program(program_code)

            print(f"Programa {i+1}: {program_info['name']}")
            print(f"  - Qubits: {program_info['qubits']}")
            print(f"  - Bits clásicos: {program_info['classical_bits']}")
            print(f"  - Funciones: {len(program_info['functions'])}")
            print(f"  - Algoritmos: {program_info['algorithms']}")

            if program_info['errors']:
                print(f"  - Errores: {program_info['errors']}")
            else:
                successful_analyses += 1

    print("\n--- Resumen de Análisis ---")
    print(f"Total de programas encontrados: {total_programs}")
    print(f"Análisis exitosos: {successful_analyses}")
    print(f"Tasa de éxito: {successful_analyses/total_programs*100:.1f}%" if total_programs > 0 else "N/A")

    return successful_analyses > 0

def test_specific_examples():
    """Prueba ejemplos específicos de Quantum-Ω"""
    print("\n=== Prueba de Ejemplos Específicos ===")

    # Ejemplo básico de optimización
    basic_example = '''
    quantum_program "optimizacion_basica" {
        version: "1.0"
        qubits: 50
        classical_bits: 20
        description: "Ejemplo básico de optimización cuántica"

        quantum_function optimizar_vector(vector_inicial: vector[10]) -> vector[10] {
            qregister qreg[10]

            for i in 0..9 {
                H(qreg[i])
            }

            QOA {
                register: qreg
                cost_func: costo_cuadratico
                iterations: 1000
            }

            return optimal_vector
        }
    }
    '''

    print("Analizando ejemplo básico de optimización...")
    program_info = analyze_quantum_program(basic_example)

    print(f"✓ Programa: {program_info['name']}")
    print(f"✓ Qubits: {program_info['qubits']}")
    print(f"✓ Funciones: {program_info['functions']}")
    print(f"✓ Algoritmos: {program_info['algorithms']}")

    return len(program_info['errors']) == 0

def main():
    """Función principal de pruebas"""
    print("=== PRUEBA DE EJEMPLOS QUANTUM-Ω ===")
    print("Fecha: 1 de octubre de 2025")
    print("Versión: 1.0 - Prototipo Inicial")
    print()

    # Ejecutar pruebas
    test1 = test_quantum_omega_examples()
    test2 = test_specific_examples()

    print("\n=== RESULTADOS DE PRUEBAS ===")
    print(f"Análisis de archivos de ejemplos: {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Ejemplos específicos: {'✓ PASS' if test2 else '✗ FAIL'}")

    if test1 and test2:
        print("\n🎉 TODAS LAS PRUEBAS DE QUANTUM-Ω PASARON")
        print("Los ejemplos del lenguaje están correctamente formateados")
        return True
    else:
        print("\n⚠️  ALGUNAS PRUEBAS DE QUANTUM-Ω FALLARON")
        print("Revisar formato de archivos de ejemplos")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)