#!/usr/bin/env python3
"""
Pruebas de Integración - CORA-Quantum Assistant
Validación completa de mecanismos de minimización de tokens y leyes físicas
Fecha: 1 de octubre de 2025
Versión: 1.0 - Pruebas de Integración Inicial
"""

import unittest
import numpy as np
import time
import sys
import os

# Agregar directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cora_quantum_assistant.core.token_minimization import (
    TokenMinimizationManager,
    IntelligentCache,
    QuantumRegenerationEngine,
    SequenceReutilizationOptimizer
)

from cora_quantum_assistant.core.physics_integration import (
    TokenPhysicsIntegrator,
    PhysicsAwareOptimizer,
    QuantumErrorCorrector,
    PhysicalConstraints
)

from cora_quantum_assistant.core.cora_quantum_assistant import CORAQuantumAssistant


class TestIntelligentCache(unittest.TestCase):
    """Pruebas para el sistema de caché inteligente"""

    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.cache = IntelligentCache(max_size=100, ttl=3600.0)

    def test_cache_storage_and_retrieval(self):
        """Prueba almacenamiento y recuperación del caché"""
        # Secuencia de comandos de prueba
        test_sequence = ["H(q[0])", "CNOT(q[0], q[1])", "measure(q[0])"]
        test_result = {"counts": {"00": 512, "11": 512}}

        # Almacenar en caché
        cache_key = self.cache.store(test_sequence, test_result)

        # Verificar almacenamiento
        self.assertIsNotNone(cache_key)
        self.assertEqual(len(self.cache.cache), 1)

        # Recuperar del caché
        retrieved_result = self.cache.retrieve(test_sequence)

        # Verificar recuperación
        self.assertEqual(retrieved_result, test_result)

    def test_cache_similarity_detection(self):
        """Prueba detección de similitud entre comandos"""
        # Secuencias similares
        seq1 = ["H(q[0])", "CNOT(q[0], q[1])", "H(q[1])"]
        seq2 = ["H(q[1])", "CNOT(q[1], q[0])", "H(q[0])"]

        # Almacenar primera secuencia
        self.cache.store(seq1, {"result": "test1"})

        # Buscar comandos similares
        similar_commands = self.cache.get_similar_commands(seq2, threshold=0.5)

        # Debería encontrar similitud
        self.assertGreater(len(similar_commands), 0)

    def test_cache_statistics(self):
        """Prueba generación de estadísticas del caché"""
        # Almacenar múltiples entradas
        for i in range(5):
            sequence = [f"cmd_{i}(q[{i}])"]
            self.cache.store(sequence, {"iteration": i})

        # Obtener estadísticas
        stats = self.cache.get_cache_statistics()

        # Verificar estadísticas
        self.assertEqual(stats['total_entries'], 5)
        self.assertGreaterEqual(stats['estimated_hit_rate'], 0.0)
        self.assertLessEqual(stats['estimated_hit_rate'], 1.0)


class TestQuantumRegenerationEngine(unittest.TestCase):
    """Pruebas para el motor de autoregeneración cuántica"""

    def setUp(self):
        """Configuración inicial"""
        self.cache = IntelligentCache()
        self.regeneration_engine = QuantumRegenerationEngine(self.cache)

    def test_quantum_pattern_analysis(self):
        """Prueba análisis de patrones cuánticos"""
        # Secuencia con patrones cuánticos conocidos
        quantum_sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "Rz(pi/4, q[0])",
            "Rx(pi/2, q[1])", "measure(q[0])", "measure(q[1])"
        ]

        # Analizar patrones
        patterns = self.regeneration_engine.analyze_quantum_patterns(quantum_sequence)

        # Debería detectar patrones
        self.assertGreater(len(patterns), 0)

        # Verificar estructura de patrones
        for pattern in patterns:
            self.assertIsNotNone(pattern.pattern_id)
            self.assertIsNotNone(pattern.state_vector)
            self.assertGreater(pattern.coherence_time, 0)

    def test_command_regeneration(self):
        """Prueba regeneración de comandos"""
        # Secuencia original
        original_sequence = [
            "H(q[0])", "H(q[1])", "CNOT(q[0], q[1])",
            "Rz(pi/4, q[0])", "Rz(pi/4, q[1])"
        ]

        # Regenerar para velocidad
        regenerated = self.regeneration_engine.regenerate_command(
            original_sequence, "speed"
        )

        # Verificar que se generó una secuencia
        self.assertIsInstance(regenerated, list)
        self.assertGreater(len(regenerated), 0)

    def test_pattern_optimization_strategies(self):
        """Prueba diferentes estrategias de optimización"""
        sequence = ["H(q[0])", "Rz(pi/4, q[0])", "Rx(pi/2, q[0])"]

        # Probar diferentes objetivos de optimización
        for target in ["speed", "accuracy", "memory"]:
            optimized = self.regeneration_engine.regenerate_command(sequence, target)

            # Verificar que se generó una secuencia válida
            self.assertIsInstance(optimized, list)


class TestSequenceReutilizationOptimizer(unittest.TestCase):
    """Pruebas para el optimizador de reutilización de secuencias"""

    def setUp(self):
        """Configuración inicial"""
        self.cache = IntelligentCache()
        self.optimizer = SequenceReutilizationOptimizer(self.cache)

    def test_repeated_subsequence_detection(self):
        """Prueba detección de subsecuencias repetidas"""
        # Secuencia con repeticiones
        sequence = [
            "H(q[0])", "Rz(pi/4, q[0])", "H(q[0])", "Rz(pi/4, q[0])",
            "H(q[1])", "Rz(pi/4, q[1])", "H(q[1])", "Rz(pi/4, q[1])"
        ]

        # Analizar oportunidades de reutilización
        opportunities = self.optimizer.analyze_reutilization_opportunities(sequence)

        # Debería detectar subsecuencias repetidas
        repeated = opportunities['repeated_subsequences']
        self.assertGreater(len(repeated), 0)

    def test_common_pattern_identification(self):
        """Prueba identificación de patrones comunes"""
        # Secuencia con patrones conocidos
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "H(q[1])",  # Patrón Bell
            "Rx(pi/2, q[0])", "Ry(pi/2, q[1])", "Rz(pi/2, q[0])"  # Rotaciones
        ]

        opportunities = self.optimizer.analyze_reutilization_opportunities(sequence)

        # Debería identificar patrones comunes
        common_patterns = opportunities['common_patterns']
        self.assertGreater(len(common_patterns), 0)

    def test_sequence_optimization(self):
        """Prueba optimización de secuencias"""
        # Secuencia con oportunidades de optimización
        sequence = [
            "H(q[0])", "H(q[0])",  # Operación redundante
            "Rz(pi/4, q[0])", "Rz(pi/8, q[0])",  # Pueden fusionarse
            "X(q[1])", "X(q[1])"  # Operación redundante
        ]

        # Optimizar secuencia
        optimized = self.optimizer.create_optimized_sequence(sequence, "auto")

        # Debería producir una secuencia válida
        self.assertIsInstance(optimized, list)

        # Podría ser más corta debido a optimizaciones
        # (aunque no garantizado en todos los casos)


class TestPhysicsAwareOptimizer(unittest.TestCase):
    """Pruebas para el optimizador consciente de física"""

    def setUp(self):
        """Configuración inicial"""
        self.optimizer = PhysicsAwareOptimizer()

    def test_physical_constraints_application(self):
        """Prueba aplicación de restricciones físicas"""
        # Secuencia de comandos
        sequence = [
            "H(q[0])", "Rz(pi/4, q[0])", "Rx(pi/2, q[0])",
            "CNOT(q[0], q[1])", "measure(q[0])"
        ]

        # Aplicar restricciones físicas
        constrained = self.optimizer.apply_physical_constraints(sequence)

        # Debería retornar una secuencia válida
        self.assertIsInstance(constrained, list)
        self.assertEqual(len(constrained), len(sequence))

    def test_physical_cost_calculation(self):
        """Prueba cálculo de costo físico"""
        sequence = ["H(q[0])", "CNOT(q[0], q[1])", "QFT(q[0], q[1])"]

        # Calcular costo físico
        cost = self.optimizer.calculate_physical_cost(sequence)

        # Debería ser un valor positivo
        self.assertGreater(cost, 0)

        # QFT debería aumentar significativamente el costo
        qft_cost = self.optimizer.calculate_physical_cost(["QFT(q[0])"])
        self.assertGreater(qft_cost, cost / len(sequence))

    def test_decoherence_models(self):
        """Prueba diferentes modelos de decoherencia"""
        sequence = ["H(q[0])", "CNOT(q[0], q[1])"]

        for model in ['T1_T2', 'amplitude_damping', 'phase_damping', 'depolarizing']:
            # Cambiar modelo de decoherencia
            self.optimizer.constraints.decoherence_model = model

            # Calcular costo con modelo específico
            cost = self.optimizer.calculate_physical_cost(sequence)

            # Debería producir un costo válido
            self.assertIsInstance(cost, float)
            self.assertGreaterEqual(cost, 0)


class TestQuantumErrorCorrector(unittest.TestCase):
    """Pruebas para el corrector de errores cuánticos"""

    def setUp(self):
        """Configuración inicial"""
        physics_optimizer = PhysicsAwareOptimizer()
        self.error_corrector = QuantumErrorCorrector(physics_optimizer)

    def test_error_pattern_analysis(self):
        """Prueba análisis de patrones de errores"""
        # Secuencia con operaciones propensas a errores
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "CCNOT(q[0], q[1], q[2])",
            "QFT(q[0], q[1], q[2])", "measure(q[0])"
        ]

        # Analizar patrones de errores
        analysis = self.error_corrector.analyze_error_patterns(sequence)

        # Debería identificar operaciones propensas a errores
        self.assertGreater(len(analysis['error_prone_operations']), 0)

        # Debería generar recomendaciones de corrección
        self.assertIsInstance(analysis['recommended_corrections'], list)

    def test_error_classification(self):
        """Prueba clasificación de tipos de errores"""
        # Probar diferentes tipos de operaciones
        test_cases = [
            ("CNOT(q[0], q[1])", "gate_error"),
            ("measure(q[0])", "measurement_error"),
            ("QFT(q[0])", "algorithmic_error")
        ]

        for command, expected_type in test_cases:
            error_type = self.error_corrector._classify_error_type(command)
            self.assertEqual(error_type, expected_type)


class TestTokenPhysicsIntegrator(unittest.TestCase):
    """Pruebas para el integrador de física y tokens"""

    def setUp(self):
        """Configuración inicial"""
        self.integrator = TokenPhysicsIntegrator()

    def test_physics_aware_minimization(self):
        """Prueba minimización consciente de física"""
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "Rz(pi/4, q[0])",
            "Rx(pi/2, q[1])", "measure(q[0])"
        ]

        # Ejecutar optimización física
        result = self.integrator.optimize_with_physics_aware_minimization(
            sequence, "balanced"
        )

        # Verificar resultado
        self.assertTrue(result['success'])
        self.assertIsInstance(result['physics_corrected_sequence'], list)
        self.assertGreater(result['physical_cost'], 0)
        self.assertIsInstance(result['quantum_effectiveness'], dict)

    def test_physics_aware_recommendations(self):
        """Prueba generación de recomendaciones físicas"""
        sequence = [
            "H(q[0])", "QFT(q[0], q[1])", "CNOT(q[0], q[1])",
            "measure(q[0])", "measure(q[1])"
        ]

        # Obtener recomendaciones
        recommendations = self.integrator.get_physics_aware_recommendations(sequence)

        # Verificar estructura de recomendaciones
        self.assertIsInstance(recommendations, dict)
        self.assertIn('physical_optimizations', recommendations)
        self.assertIn('error_corrections', recommendations)
        self.assertIn('coherence_improvements', recommendations)
        self.assertIn('overall_assessment', recommendations)


class TestCORAQuantumAssistantIntegration(unittest.TestCase):
    """Pruebas de integración completa del asistente cuántico"""

    def setUp(self):
        """Configuración inicial"""
        self.assistant = CORAQuantumAssistant()

    def test_token_minimization_integration(self):
        """Prueba integración de minimización de tokens"""
        sequence = [
            "H(q[0])", "H(q[1])", "CNOT(q[0], q[1])",
            "Rz(pi/4, q[0])", "Rz(pi/4, q[1])"
        ]

        # Ejecutar minimización integrada
        result = self.assistant.token_minimizer.minimize_tokens(sequence, "auto")

        # Verificar integración
        self.assertTrue(result['success'])
        self.assertIsInstance(result['optimized_sequence'], list)

    def test_physics_integration(self):
        """Prueba integración física"""
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "measure(q[0])"
        ]

        # Ejecutar optimización física integrada
        result = self.assistant.execute_physics_aware_optimization(sequence, "balanced")

        # Verificar integración
        self.assertTrue(result['success'])
        self.assertIsInstance(result['combined_result'], list)
        self.assertGreater(result['physical_cost'], 0)

    def test_pattern_analysis_integration(self):
        """Prueba análisis integrado de patrones"""
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "H(q[1])",
            "Rz(pi/4, q[0])", "Rx(pi/2, q[1])"
        ]

        # Ejecutar análisis integrado
        analysis = self.assistant.analyze_physical_quantum_patterns(sequence)

        # Verificar análisis completo
        self.assertIsInstance(analysis['quantum_patterns'], list)
        self.assertIsInstance(analysis['reutilization_opportunities'], dict)
        self.assertIsInstance(analysis['physics_recommendations'], dict)
        self.assertIsInstance(analysis['physical_constraints'], dict)

    def test_system_status_integration(self):
        """Prueba estado integrado del sistema"""
        # Obtener estado del sistema
        status = self.assistant.get_system_status()

        # Verificar integración completa
        self.assertTrue(status['quantum_processor_ready'])
        self.assertTrue(status['token_minimization']['enabled'])
        self.assertTrue(status['physics_integration']['enabled'])

        # Verificar métricas físicas
        self.assertIsInstance(status['physics_integration']['temperature'], float)
        self.assertIsInstance(status['physics_integration']['coherence_time'], float)


class TestEndToEndWorkflow(unittest.TestCase):
    """Pruebas de flujo completo end-to-end"""

    def setUp(self):
        """Configuración inicial"""
        self.assistant = CORAQuantumAssistant()

    def test_complete_optimization_workflow(self):
        """Prueba flujo completo de optimización"""
        # Secuencia inicial compleja
        initial_sequence = [
            "H(q[0])", "H(q[1])", "H(q[2])",
            "CNOT(q[0], q[1])", "CNOT(q[1], q[2])",
            "Rz(pi/4, q[0])", "Rz(pi/4, q[1])", "Rz(pi/4, q[2])",
            "Rx(pi/2, q[0])", "Rx(pi/2, q[1])", "Rx(pi/2, q[2])",
            "H(q[0])", "H(q[1])", "H(q[2])",
            "measure(q[0])", "measure(q[1])", "measure(q[2])"
        ]

        # 1. Análisis inicial de patrones
        initial_analysis = self.assistant.analyze_quantum_patterns(initial_sequence)
        initial_patterns = len(initial_analysis['quantum_patterns'])

        # 2. Minimización de tokens
        minimization_result = self.assistant.token_minimizer.minimize_tokens(
            initial_sequence, "auto"
        )

        # 3. Optimización física
        physics_result = self.assistant.execute_physics_aware_optimization(
            initial_sequence, "balanced"
        )

        # 4. Análisis final
        final_analysis = self.assistant.analyze_physical_quantum_patterns(
            physics_result['combined_result']
        )

        # Verificaciones
        self.assertTrue(minimization_result['success'])
        self.assertTrue(physics_result['success'])

        # El proceso completo debería haber aplicado optimizaciones
        self.assertIsInstance(physics_result['combined_result'], list)

        # Debería haber métricas físicas válidas
        self.assertGreater(physics_result['physical_cost'], 0)
        self.assertGreaterEqual(physics_result['quantum_effectiveness'], 0)
        self.assertLessEqual(physics_result['quantum_effectiveness'], 1)

    def test_cache_effectiveness_over_time(self):
        """Prueba efectividad del caché a lo largo del tiempo"""
        # Ejecutar múltiples operaciones similares
        base_sequence = ["H(q[0])", "CNOT(q[0], q[1])", "measure(q[0])"]

        execution_times = []

        for i in range(3):
            # Variar ligeramente la secuencia
            sequence = base_sequence.copy()
            if i > 0:
                sequence.insert(1, f"Rz(pi/{2**i}, q[0])")

            # Medir tiempo de minimización
            start_time = time.time()
            result = self.assistant.token_minimizer.minimize_tokens(sequence, "auto")
            end_time = time.time()

            execution_times.append(end_time - start_time)

            # Verificar éxito
            self.assertTrue(result['success'])

        # Los tiempos deberían ser consistentes (no degradación significativa)
        # Nota: En un sistema real con caché efectivo, los tiempos podrían mejorar
        for i in range(1, len(execution_times)):
            # Permitir variación razonable (±50%)
            ratio = execution_times[i] / execution_times[0]
            self.assertGreater(ratio, 0.5)  # No más de 2x más lento
            self.assertLess(ratio, 2.0)     # No más de 2x más rápido (evitar falsos positivos)


def run_integration_tests():
    """Ejecuta todas las pruebas de integración"""
    print("=== Pruebas de Integración - CORA-Quantum Assistant ===")
    print("Fecha: 1 de octubre de 2025")
    print("Versión: 1.0 - Pruebas de Integración Inicial")
    print()

    # Crear suite de pruebas
    test_classes = [
        TestIntelligentCache,
        TestQuantumRegenerationEngine,
        TestSequenceReutilizationOptimizer,
        TestPhysicsAwareOptimizer,
        TestQuantumErrorCorrector,
        TestTokenPhysicsIntegrator,
        TestCORAQuantumAssistantIntegration,
        TestEndToEndWorkflow
    ]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todas las pruebas
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Reportar resultados
    print("\n=== Resumen de Pruebas ===")
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallas: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")

    if result.errors:
        print("\nErrores encontrados:")
        for test, error in result.errors:
            print(f"- {test}: {error.split(chr(10))[0]}")

    if result.failures:
        print("\nFallas encontradas:")
        for test, failure in result.failures:
            print(f"- {test}: {failure.split(chr(10))[0]}")

    # Retornar código de salida basado en resultados
    if result.wasSuccessful():
        print("\n✅ Todas las pruebas pasaron exitosamente")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1


if __name__ == "__main__":
    exit_code = run_integration_tests()
    sys.exit(exit_code)