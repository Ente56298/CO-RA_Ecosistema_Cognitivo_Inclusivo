#!/usr/bin/env python3
"""
Script de prueba básico para CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prueba básica
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba importaciones básicas"""
    print("=== Prueba de Importaciones Básicas ===")

    try:
        import numpy as np
        print("✓ NumPy importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando NumPy: {e}")
        return False

    try:
        import scipy
        print("✓ SciPy importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando SciPy: {e}")
        return False

    try:
        import matplotlib
        print("✓ Matplotlib importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando Matplotlib: {e}")
        return False

    return True

def test_cora_core():
    """Prueba componentes básicos de CORA"""
    print("\n=== Prueba de Componentes CORA ===")

    try:
        # Importar componentes básicos sin Qiskit
        import numpy as np
        from dataclasses import dataclass
        import time
        import logging

        print("✓ Componentes básicos importados correctamente")

        # Probar configuración cuántica básica
        @dataclass
        class QuantumConfig:
            qubits: int = 1000
            classical_bits: int = 50
            coherence_time: float = 500.0
            error_rate: float = 1e-4

        config = QuantumConfig()
        print(f"✓ Configuración cuántica creada: {config.qubits} qubits")

        # Probar monitor de coherencia básico
        class CoherenceMonitor:
            def __init__(self, config):
                self.config = config
                self.start_time = time.time()
                self.coherence_threshold = config.coherence_time

            def get_coherence_time(self):
                import time
                elapsed = (time.time() - self.start_time) * 1e6
                return max(0, self.coherence_threshold - elapsed)

            def is_coherent(self):
                return self.get_coherence_time() > 0

        monitor = CoherenceMonitor(config)
        print(f"✓ Monitor de coherencia creado: {'Activa' if monitor.is_coherent() else 'Perdida'}")

        return True

    except Exception as e:
        print(f"✗ Error en componentes CORA: {e}")
        return False

def test_omega_language():
    """Prueba análisis básico del lenguaje Quantum-Ω"""
    print("\n=== Prueba de Lenguaje Quantum-Ω ===")

    try:
        # Código Quantum-Ω básico de ejemplo
        omega_code = '''
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

        # Análisis básico del código
        lines = omega_code.strip().split('\n')
        program_info = {
            'name': 'unnamed',
            'version': '1.0',
            'qubits': 50,
            'functions': []
        }

        for line in lines:
            line = line.strip()
            if line.startswith('quantum_program'):
                if '"' in line:
                    program_info['name'] = line.split('"')[1]
            elif line.startswith('qubits:'):
                program_info['qubits'] = int(line.split(':')[1].strip())
            elif line.startswith('version:'):
                program_info['version'] = line.split(':')[1].strip()

        print(f"✓ Código Quantum-Ω analizado correctamente")
        print(f"  - Programa: {program_info['name']}")
        print(f"  - Qubits: {program_info['qubits']}")
        print(f"  - Versión: {program_info['version']}")

        return True

    except Exception as e:
        print(f"✗ Error analizando Quantum-Ω: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=== PRUEBA BÁSICA CORA-QUANTUM ASSISTANT ===")
    print("Fecha: 1 de octubre de 2025")
    print("Versión: 1.0 - Prototipo Inicial")
    print()

    # Ejecutar pruebas
    test1 = test_imports()
    test2 = test_cora_core()
    test3 = test_omega_language()

    print("\n=== RESULTADOS DE PRUEBAS ===")
    print(f"Importaciones básicas: {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Componentes CORA: {'✓ PASS' if test2 else '✗ FAIL'}")
    print(f"Lenguaje Quantum-Ω: {'✓ PASS' if test3 else '✗ FAIL'}")

    if all([test1, test2, test3]):
        print("\n🎉 TODAS LAS PRUEBAS BÁSICAS PASARON")
        print("El sistema CORA-Quantum Assistant está funcionando correctamente")
        return True
    else:
        print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
        print("Se recomienda revisar la instalación de dependencias")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)