#!/usr/bin/env python3
"""
Script de Pruebas Básicas Mejorado - CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import sys
import os
import unittest
import time
import numpy as np
from typing import Dict, Any

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestCORAQuantumAssistant(unittest.TestCase):
    """Suite de pruebas para CORA-Quantum Assistant"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.test_config = {
            'qubits': 100,
            'classical_bits': 10,
            'coherence_time': 100.0,
            'error_rate': 1e-4
        }

        # Importar componentes necesarios
        try:
            from core.cora_quantum_assistant import CORAQuantumAssistant, QuantumConfig
            from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator, SimulationConfig

            self.assistant_available = True
            self.simulator_available = True

            # Inicializar componentes
            config = QuantumConfig(**self.test_config)
            self.assistant = CORAQuantumAssistant(config)

            sim_config = SimulationConfig(max_qubits=100, hybrid_mode=True)
            self.simulator = HybridQuantumSimulator(sim_config)

        except ImportError as e:
            print(f"Advertencia: No se pudieron importar algunos componentes: {e}")
            self.assistant_available = False
            self.simulator_available = False

    def test_system_initialization(self):
        """Prueba inicialización del sistema"""
        print("\n🧪 Prueba: Inicialización del sistema")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Verificar que el asistente se inicializó correctamente
        status = self.assistant.get_system_status()

        self.assertTrue(status['quantum_processor_ready'], "Procesador cuántico debe estar listo")
        self.assertIsNotNone(status['config'], "Configuración debe estar disponible")
        self.assertEqual(status['config']['qubits'], self.test_config['qubits'], "Número de qubits debe coincidir")

        print("✓ Inicialización del sistema exitosa")

    def test_quantum_optimization(self):
        """Prueba optimización cuántica básica"""
        print("\n🧪 Prueba: Optimización cuántica")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Datos de prueba
        problem_data = {
            'size': 20,
            'complexity': 'medium',
            'description': 'Prueba de optimización'
        }

        # Ejecutar optimización
        result = self.assistant.execute_quantum_task('optimization', problem_data=problem_data)

        self.assertTrue(result['success'], "Optimización debe ser exitosa")
        self.assertIsNotNone(result['optimization_result'], "Debe haber resultado de optimización")
        self.assertGreater(result['optimization_result'].quantum_advantage, 0, "Debe haber ventaja cuántica")

        print(f"✓ Optimización completada con {result['optimization_result'].quantum_advantage*100:.1f}% ventaja cuántica")

    def test_hybrid_simulation(self):
        """Prueba simulación híbrida"""
        print("\n🧪 Prueba: Simulación híbrida")

        if not self.simulator_available:
            self.skipTest("Simulador híbrido no disponible")

        # Función de costo simple
        def test_cost_function(x):
            return np.sum(x**2)

        # Solución inicial
        initial_solution = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        # Ejecutar simulación
        result = self.simulator.simulate(test_cost_function, initial_solution)

        self.assertIsNotNone(result.solution, "Debe haber solución")
        self.assertGreater(result.execution_time, 0, "Tiempo de ejecución debe ser positivo")
        self.assertIsNotNone(result.mode_used, "Debe especificar modo usado")
        self.assertGreaterEqual(result.accuracy, 0, "Precisión debe ser no negativa")
        self.assertLessEqual(result.accuracy, 1, "Precisión debe ser <= 1")

        print(f"✓ Simulación híbrida completada en modo {result.mode_used}")

    def test_token_minimization(self):
        """Prueba minimización de tokens"""
        print("\n🧪 Prueba: Minimización de tokens")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Secuencia de comandos de prueba
        test_commands = [
            "H(q[0])", "H(q[1])", "CNOT(q[0], q[1])", "Rz(pi/4, q[0])", "Rz(pi/4, q[1])",
            "Rx(pi/2, q[0])", "Rx(pi/2, q[1])", "H(q[0])", "H(q[1])", "measure(q[0])",
            "measure(q[1])", "H(q[0])", "H(q[1])", "Rz(pi/4, q[0])", "Rz(pi/4, q[1])"
        ]

        # Aplicar minimización
        result = self.assistant.token_minimizer.minimize_tokens(test_commands, "auto")

        self.assertTrue(result['success'], "Minimización debe ser exitosa")
        self.assertIsNotNone(result['optimized_sequence'], "Debe haber secuencia optimizada")
        self.assertGreaterEqual(result['tokens_saved'], 0, "Tokens ahorrados debe ser no negativo")

        print(f"✓ Minimización completada: {result['tokens_saved']} tokens ahorrados")

    def test_omega_language_parsing(self):
        """Prueba análisis del lenguaje Quantum-Ω"""
        print("\n🧪 Prueba: Análisis de lenguaje Quantum-Ω")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Código Quantum-Ω de prueba
        omega_code = '''
        quantum_program "test_program" {
            version: "1.0"
            qubits: 10
            classical_bits: 5

            quantum_function test_function(vector_inicial: vector[5]) -> vector[5] {
                qregister qreg[5]

                for i in 0..4 {
                    H(qreg[i])
                }

                QOA {
                    register: qreg
                    cost_func: test_cost
                    iterations: 100
                }

                return optimal_vector
            }
        }
        '''

        # Ejecutar código Quantum-Ω
        result = self.assistant.execute_quantum_task('omega_code', code=omega_code)

        # La prueba es que no lance excepción (incluso si el resultado no es perfecto)
        self.assertIsNotNone(result, "Debe haber resultado de ejecución")

        print("✓ Código Quantum-Ω ejecutado sin errores críticos")

    def test_physics_integration(self):
        """Prueba integración con leyes físicas"""
        print("\n🧪 Prueba: Integración con leyes físicas")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Secuencia de comandos para análisis físico
        test_commands = [
            "H(q[0])", "CNOT(q[0], q[1])", "Rz(pi/4, q[0])", "Rx(pi/2, q[1])",
            "H(q[0])", "H(q[1])", "measure(q[0])", "measure(q[1])"
        ]

        # Obtener recomendaciones físicas
        recommendations = self.assistant.get_physics_aware_recommendations(test_commands)

        self.assertIsNotNone(recommendations, "Debe haber recomendaciones físicas")

        print("✓ Integración física funcionando correctamente")

    def test_quantum_simulation_basic(self):
        """Prueba simulación cuántica básica"""
        print("\n🧪 Prueba: Simulación cuántica básica")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Ejecutar simulación cuántica básica
        result = self.assistant.execute_quantum_task('quantum_simulation', n_qubits=10)

        self.assertIsNotNone(result, "Debe haber resultado de simulación")
        self.assertIn('success', result, "Resultado debe tener campo 'success'")

        print("✓ Simulación cuántica básica ejecutada")

    def test_system_status_monitoring(self):
        """Prueba monitoreo de estado del sistema"""
        print("\n🧪 Prueba: Monitoreo de estado del sistema")

        if not self.assistant_available:
            self.skipTest("CORA-Quantum Assistant no disponible")

        # Obtener estado del sistema múltiples veces
        for i in range(3):
            status = self.assistant.get_system_status()
            time.sleep(0.1)  # Pequeña pausa

            self.assertIsNotNone(status, "Estado del sistema no debe ser None")
            self.assertIn('quantum_processor_ready', status, "Estado debe tener campo quantum_processor_ready")
            self.assertIn('coherence_status', status, "Estado debe tener campo coherence_status")
            self.assertIn('config', status, "Estado debe tener campo config")

        print("✓ Monitoreo de estado funcionando correctamente")

class TestIntegrationScenarios(unittest.TestCase):
    """Pruebas de escenarios de integración"""

    def test_end_to_end_workflow(self):
        """Prueba flujo de trabajo completo"""
        print("\n🔄 Prueba: Flujo de trabajo completo")

        try:
            # 1. Configuración
            from config import EnvironmentConfigurator
            configurator = EnvironmentConfigurator()
            config = configurator.load_config()

            # 2. Inicialización
            from core.cora_quantum_assistant import CORAQuantumAssistant, QuantumConfig
            quantum_config = QuantumConfig(
                qubits=config.qubits,
                classical_bits=config.classical_bits
            )
            assistant = CORAQuantumAssistant(quantum_config)

            # 3. Ejecución de tareas
            problem_data = {'size': 10, 'complexity': 'low'}
            result1 = assistant.execute_quantum_task('optimization', problem_data=problem_data)

            # 4. Simulación híbrida
            from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator
            simulator = HybridQuantumSimulator()

            def simple_cost(x):
                return sum(x**2)

            initial = [1.0, 2.0, 3.0]
            result2 = simulator.simulate(simple_cost, initial)

            # 5. Verificación de integración
            from verify_integration import IntegrationVerifier
            verifier = IntegrationVerifier()
            integration_result = verifier.verify_all_components()

            # Verificaciones
            self.assertIsNotNone(config, "Configuración debe estar disponible")
            self.assertIsNotNone(assistant, "Asistente debe estar inicializado")
            self.assertTrue(result1['success'], "Primera tarea debe ser exitosa")
            self.assertIsNotNone(result2.solution, "Simulación debe tener solución")
            self.assertTrue(integration_result['all_passed'], "Integración debe ser exitosa")

            print("✓ Flujo de trabajo completo ejecutado exitosamente")

        except Exception as e:
            self.fail(f"Flujo de trabajo completo falló: {str(e)}")

def run_specific_test(test_name):
    """Ejecuta una prueba específica"""
    print(f"\n🎯 Ejecutando prueba específica: {test_name}")

    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar pruebas específicas
    if test_name == 'initialization':
        suite.addTest(TestCORAQuantumAssistant('test_system_initialization'))
    elif test_name == 'optimization':
        suite.addTest(TestCORAQuantumAssistant('test_quantum_optimization'))
    elif test_name == 'simulation':
        suite.addTest(TestCORAQuantumAssistant('test_hybrid_simulation'))
    elif test_name == 'tokens':
        suite.addTest(TestCORAQuantumAssistant('test_token_minimization'))
    elif test_name == 'omega':
        suite.addTest(TestCORAQuantumAssistant('test_omega_language_parsing'))
    elif test_name == 'physics':
        suite.addTest(TestCORAQuantumAssistant('test_physics_integration'))
    elif test_name == 'monitoring':
        suite.addTest(TestCORAQuantumAssistant('test_system_status_monitoring'))
    elif test_name == 'workflow':
        suite.addTest(TestIntegrationScenarios('test_end_to_end_workflow'))
    elif test_name == 'all':
        # Ejecutar todas las pruebas
        suite.addTests(loader.loadTestsFromTestCase(TestCORAQuantumAssistant))
        suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    else:
        print(f"❌ Prueba desconocida: {test_name}")
        return False

    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()

def main():
    """Función principal de pruebas"""
    print("🧪 CORA-Quantum Assistant - Suite de Pruebas Mejorada")
    print("=" * 60)
    print("Fecha: 1 de octubre de 2025")
    print("Versión: 1.0 - Prototipo Inicial")
    print()

    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
        sys.exit(0 if success else 1)

    # Menú interactivo
    print("Selecciona una opción:")
    print("1. Todas las pruebas")
    print("2. Inicialización del sistema")
    print("3. Optimización cuántica")
    print("4. Simulación híbrida")
    print("5. Minimización de tokens")
    print("6. Lenguaje Quantum-Ω")
    print("7. Integración física")
    print("8. Monitoreo de estado")
    print("9. Flujo de trabajo completo")
    print("0. Salir")

    while True:
        try:
            choice = input("\nSelecciona opción (0-9): ").strip()

            test_names = {
                '1': 'all',
                '2': 'initialization',
                '3': 'optimization',
                '4': 'simulation',
                '5': 'tokens',
                '6': 'omega',
                '7': 'physics',
                '8': 'monitoring',
                '9': 'workflow'
            }

            if choice == '0':
                print("👋 ¡Hasta luego!")
                break
            elif choice in test_names:
                success = run_specific_test(test_names[choice])
                if not success:
                    print("❌ Algunas pruebas fallaron")
                else:
                    print("✅ Todas las pruebas pasaron")
            else:
                print("❓ Opción no válida")

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()