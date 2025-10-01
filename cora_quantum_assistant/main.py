#!/usr/bin/env python3
"""
Script Principal de Inicialización - CORA-Quantum Assistant
Primer prototipo funcional básico
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import sys
import os
import argparse
import time
from typing import Dict, Any
import logging

# Agregar el directorio actual al path para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CORAQuantumLauncher:
    """Lanzador principal del CORA-Quantum Assistant"""

    def __init__(self):
        self.assistant = None
        self.simulator = None
        self.system_status = {
            'initialized': False,
            'components_ready': False,
            'ready_for_tasks': False
        }

    def initialize_system(self, config: Dict[str, Any] = None) -> bool:
        """Inicializa el sistema CORA-Quantum completo"""
        print("🚀 Inicializando CORA-Quantum Assistant...")
        print("=" * 60)

        try:
            # 1. Inicializar asistente cuántico principal
            print("📡 Inicializando asistente cuántico principal...")
            from core.cora_quantum_assistant import CORAQuantumAssistant, QuantumConfig

            quantum_config = QuantumConfig(
                qubits=config.get('qubits', 1000),
                classical_bits=config.get('classical_bits', 50),
                coherence_time=config.get('coherence_time', 500.0),
                error_rate=config.get('error_rate', 1e-4)
            )

            self.assistant = CORAQuantumAssistant(quantum_config)
            print("   ✓ Asistente cuántico inicializado")

            # 2. Inicializar simulador híbrido
            print("🔬 Inicializando simulador híbrido...")
            from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator, SimulationConfig

            sim_config = SimulationConfig(
                max_qubits=config.get('max_qubits', 1000),
                classical_memory_limit=config.get('memory_limit', 8 * 1024 * 1024 * 1024),
                quantum_error_rate=config.get('quantum_error_rate', 1e-4),
                hybrid_mode=config.get('hybrid_mode', True)
            )

            self.simulator = HybridQuantumSimulator(sim_config)
            print("   ✓ Simulador híbrido inicializado")

            # 3. Verificar estado del sistema
            print("🔍 Verificando estado del sistema...")
            system_status = self.assistant.get_system_status()
            sim_status = self.simulator.get_system_status()

            print(f"   ✓ Procesador cuántico: {'Listo' if system_status['quantum_processor_ready'] else 'No listo'}")
            print(f"   ✓ Coherencia: {'Activa' if system_status['coherence_status'] else 'Perdida'}")
            print(f"   ✓ Qubits disponibles: {system_status['config']['qubits']}")
            print(f"   ✓ Simulador híbrido: {'Listo' if sim_status['hybrid_mode_enabled'] else 'No listo'}")

            # 4. Actualizar estado del sistema
            self.system_status['initialized'] = True
            self.system_status['components_ready'] = True
            self.system_status['ready_for_tasks'] = True

            print("\n🎉 CORA-Quantum Assistant inicializado exitosamente!")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"❌ Error durante la inicialización: {str(e)}")
            logger.error(f"Error de inicialización: {str(e)}")
            return False

    def run_demonstration(self) -> bool:
        """Ejecuta demostración completa del sistema"""
        if not self.system_status['ready_for_tasks']:
            print("❌ Sistema no está listo para ejecutar tareas")
            return False

        print("\n🧪 Ejecutando demostración completa del sistema...")
        print("=" * 60)

        try:
            # 1. Demostración de minimización de tokens
            print("\n📝 Demostración de Minimización de Tokens:")
            print("-" * 40)

            sample_commands = [
                "H(q[0])", "H(q[1])", "CNOT(q[0], q[1])", "Rz(pi/4, q[0])", "Rz(pi/4, q[1])",
                "Rx(pi/2, q[0])", "Rx(pi/2, q[1])", "H(q[0])", "H(q[1])", "measure(q[0])",
                "measure(q[1])", "H(q[0])", "H(q[1])", "Rz(pi/4, q[0])", "Rz(pi/4, q[1])"
            ]

            print(f"Secuencia original: {len(sample_commands)} comandos")

            minimization_result = self.assistant.token_minimizer.minimize_tokens(sample_commands, "auto")

            if minimization_result['success']:
                print(f"✓ Tokens ahorrados: {minimization_result['tokens_saved']}")
                print(f"✓ Método usado: {minimization_result['minimization_method']}")
            else:
                print(f"✗ Error en minimización: {minimization_result.get('error', 'Error desconocido')}")

            # 2. Demostración de optimización híbrida
            print("\n⚡ Demostración de Optimización Híbrida:")
            print("-" * 40)

            problem_data = {
                'size': 50,
                'complexity': 'high',
                'description': 'Optimización de portafolio financiero cuántico'
            }

            result = self.assistant.execute_quantum_task('optimization', problem_data=problem_data)

            if result['success']:
                opt_result = result['optimization_result']
                print(f"✓ Optimización completada: {opt_result.quantum_advantage*100:.1f}% ventaja cuántica")
                print(f"✓ Tiempo de convergencia: {opt_result.convergence_time:.3f}s")
            else:
                print(f"✗ Error en optimización: {result.get('error', 'Error desconocido')}")

            # 3. Demostración del simulador híbrido
            print("\n🔬 Demostración del Simulador Híbrido:")
            print("-" * 40)

            def demo_cost_function(x):
                return sum(x**2)  # Función esfera

            initial_solution = [1.0, 2.0, 3.0, 4.0, 5.0]

            sim_result = self.simulator.simulate(demo_cost_function, initial_solution)

            print(f"✓ Modo usado: {sim_result.mode_used}")
            print(f"✓ Tiempo de ejecución: {sim_result.execution_time:.3f}s")
            print(f"✓ Precisión: {sim_result.accuracy*100:.1f}%")

            # 4. Demostración del lenguaje Quantum-Ω
            print("\n📚 Demostración del Lenguaje Quantum-Ω:")
            print("-" * 40)

            omega_code = '''
            quantum_program "demo_omega" {
                version: "1.0"
                qubits: 10
                classical_bits: 10

                quantum_function demo_optimization(vector_inicial: vector[5]) -> vector[5] {
                    qregister qreg[5]

                    for i in 0..4 {
                        H(qreg[i])
                    }

                    QOA {
                        register: qreg
                        cost_func: costo_demo
                        iterations: 100
                    }

                    return optimal_vector
                }
            }
            '''

            omega_result = self.assistant.execute_quantum_task('omega_code',
                code=omega_code,
                execution_params={'QOA': [[1, 0.1], [0.1, 1]]}
            )

            if omega_result['success']:
                print("✓ Código Quantum-Ω ejecutado exitosamente")
            else:
                print(f"✗ Error ejecutando Quantum-Ω: {omega_result.get('error', 'Error desconocido')}")

            print("\n🎉 Demostración completada exitosamente!")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"❌ Error durante la demostración: {str(e)}")
            logger.error(f"Error en demostración: {str(e)}")
            return False

    def run_interactive_mode(self):
        """Ejecuta modo interactivo"""
        if not self.system_status['ready_for_tasks']:
            print("❌ Sistema no está listo para modo interactivo")
            return

        print("\n🎯 Modo Interactivo CORA-Quantum Assistant")
        print("=" * 60)
        print("Comandos disponibles:")
        print("  demo     - Ejecutar demostración completa")
        print("  status   - Ver estado del sistema")
        print("  optimize - Ejecutar optimización personalizada")
        print("  simulate - Ejecutar simulación personalizada")
        print("  omega    - Ejecutar código Quantum-Ω")
        print("  help     - Mostrar esta ayuda")
        print("  quit     - Salir del modo interactivo")
        print()

        while True:
            try:
                command = input("CORA-Quantum> ").strip().lower()

                if command == 'quit' or command == 'exit':
                    print("👋 ¡Hasta luego!")
                    break
                elif command == 'demo':
                    self.run_demonstration()
                elif command == 'status':
                    self.show_system_status()
                elif command == 'help':
                    self.show_help()
                elif command == 'optimize':
                    self.run_custom_optimization()
                elif command == 'simulate':
                    self.run_custom_simulation()
                elif command == 'omega':
                    self.run_custom_omega()
                else:
                    print("❓ Comando no reconocido. Use 'help' para ver comandos disponibles.")

            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def show_system_status(self):
        """Muestra estado actual del sistema"""
        if self.assistant:
            status = self.assistant.get_system_status()
            print("\n📊 Estado del Sistema:")
            print(f"  Procesador cuántico: {'✓ Listo' if status['quantum_processor_ready'] else '✗ No listo'}")
            print(f"  Coherencia: {'✓ Activa' if status['coherence_status'] else '✗ Perdida'}")
            print(f"  Qubits: {status['config']['qubits']}")
            print(f"  Bits clásicos: {status['config']['classical_bits']}")
            print(f"  Tiempo de coherencia: {status['coherence_time_remaining']:.2f} μs")
            print(f"  Minimización de tokens: {'✓ Activa' if status['token_minimization']['enabled'] else '✗ Inactiva'}")
            print(f"  Entradas en caché: {status['token_minimization']['cache_entries']}")

    def show_help(self):
        """Muestra ayuda del modo interactivo"""
        print("\n📖 Ayuda - Modo Interactivo:")
        print("  demo     - Ejecuta demostración completa del sistema")
        print("  status   - Muestra estado actual del sistema")
        print("  optimize - Ejecuta optimización con parámetros personalizados")
        print("  simulate - Ejecuta simulación con parámetros personalizados")
        print("  omega    - Ejecuta código personalizado en Quantum-Ω")
        print("  help     - Muestra esta ayuda")
        print("  quit     - Sale del modo interactivo")

    def run_custom_optimization(self):
        """Ejecuta optimización personalizada"""
        try:
            print("\n⚡ Optimización Personalizada:")
            size = int(input("  Tamaño del problema (default 20): ") or "20")
            complexity = input("  Complejidad (low/medium/high, default 'medium'): ") or "medium"

            problem_data = {
                'size': size,
                'complexity': complexity,
                'description': 'Optimización personalizada'
            }

            print(f"  Ejecutando optimización de tamaño {size} con complejidad {complexity}...")
            result = self.assistant.execute_quantum_task('optimization', problem_data=problem_data)

            if result['success']:
                opt_result = result['optimization_result']
                print(f"  ✓ Completado: {opt_result.quantum_advantage*100:.1f}% ventaja cuántica")
            else:
                print(f"  ✗ Error: {result.get('error', 'Error desconocido')}")

        except Exception as e:
            print(f"❌ Error en optimización personalizada: {str(e)}")

    def run_custom_simulation(self):
        """Ejecuta simulación personalizada"""
        try:
            print("\n🔬 Simulación Personalizada:")
            size = int(input("  Tamaño del problema (default 10): ") or "10")

            def cost_function(x):
                return sum(x**2)

            initial_solution = [float(i+1) for i in range(size)]

            print(f"  Ejecutando simulación de tamaño {size}...")
            result = self.simulator.simulate(cost_function, initial_solution)

            print(f"  ✓ Modo usado: {result.mode_used}")
            print(f"  ✓ Tiempo: {result.execution_time:.3f}s")
            print(f"  ✓ Precisión: {result.accuracy*100:.1f}%")

        except Exception as e:
            print(f"❌ Error en simulación personalizada: {str(e)}")

    def run_custom_omega(self):
        """Ejecuta código Quantum-Ω personalizado"""
        try:
            print("\n📚 Código Quantum-Ω Personalizado:")
            print("Ingrese el código Quantum-Ω (presione Enter dos veces para terminar):")

            lines = []
            while True:
                line = input()
                if line == "" and (len(lines) == 0 or lines[-1] == ""):
                    break
                lines.append(line)

            omega_code = '\n'.join(lines)

            if omega_code.strip():
                print("  Ejecutando código Quantum-Ω...")
                result = self.assistant.execute_quantum_task('omega_code', code=omega_code)

                if result['success']:
                    print("  ✓ Código ejecutado exitosamente")
                else:
                    print(f"  ✗ Error: {result.get('error', 'Error desconocido')}")
            else:
                print("  ✗ No se ingresó código válido")

        except Exception as e:
            print(f"❌ Error ejecutando código Quantum-Ω: {str(e)}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='CORA-Quantum Assistant - Prototipo Básico')
    parser.add_argument('--mode', '-m', choices=['demo', 'interactive', 'status'],
                       default='interactive', help='Modo de ejecución')
    parser.add_argument('--qubits', type=int, default=1000, help='Número de qubits')
    parser.add_argument('--memory-limit', type=int, default=8*1024*1024*1024,
                       help='Límite de memoria en bytes')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Nivel de logging')

    args = parser.parse_args()

    # Configurar nivel de logging
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Crear lanzador
    launcher = CORAQuantumLauncher()

    # Configuración del sistema
    config = {
        'qubits': args.qubits,
        'classical_bits': 50,
        'coherence_time': 500.0,
        'error_rate': 1e-4,
        'max_qubits': args.qubits,
        'memory_limit': args.memory_limit,
        'quantum_error_rate': 1e-4,
        'hybrid_mode': True
    }

    # Inicializar sistema
    if not launcher.initialize_system(config):
        print("❌ Falló la inicialización del sistema")
        sys.exit(1)

    # Ejecutar según modo seleccionado
    if args.mode == 'demo':
        success = launcher.run_demonstration()
        sys.exit(0 if success else 1)
    elif args.mode == 'status':
        launcher.show_system_status()
        sys.exit(0)
    else:  # interactive
        launcher.run_interactive_mode()
        sys.exit(0)

if __name__ == "__main__":
    main()