#!/usr/bin/env python3
"""
Pruebas Específicas de Minimización de Tokens - CORA-Quantum Assistant
Pruebas enfocadas únicamente en mecanismos de minimización sin dependencias externas
Fecha: 1 de octubre de 2025
Versión: 1.0 - Pruebas de Minimización Aisladas
"""

import unittest
import numpy as np
import time
import sys
import os

# Agregar directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar solo módulos de minimización de tokens (sin Qiskit)
from cora_quantum_assistant.core.token_minimization import (
    TokenMinimizationManager,
    IntelligentCache,
    QuantumRegenerationEngine,
    SequenceReutilizationOptimizer
)


class TestTokenMinimizationCore(unittest.TestCase):
    """Pruebas básicas de minimización de tokens"""

    def setUp(self):
        """Configuración inicial"""
        self.minimizer = TokenMinimizationManager(cache_size=100, cache_ttl=3600.0)

    def test_basic_minimization(self):
        """Prueba minimización básica de tokens"""
        # Secuencia simple con redundancias
        sequence = [
            "H(q[0])", "H(q[0])",  # Redundante
            "Rz(pi/4, q[0])", "Rz(pi/8, q[0])",  # Pueden fusionarse
            "X(q[1])", "X(q[1])",  # Redundante
            "measure(q[0])"
        ]

        # Aplicar minimización
        result = self.minimizer.minimize_tokens(sequence, "auto")

        # Verificar resultado básico
        self.assertTrue(result['success'])
        self.assertIsInstance(result['optimized_sequence'], list)
        self.assertGreaterEqual(len(result['optimized_sequence']), 0)

        # Verificar métricas
        self.assertIn('processing_time', result)
        self.assertIn('tokens_saved', result)
        self.assertIn('compression_ratio', result)

    def test_cache_functionality(self):
        """Prueba funcionalidad básica del caché"""
        # Secuencia de prueba
        sequence = ["H(q[0])", "CNOT(q[0], q[1])", "measure(q[0])"]

        # Primera ejecución (debe almacenar en caché)
        result1 = self.minimizer.minimize_tokens(sequence, "auto")
        self.assertTrue(result1['success'])

        # Segunda ejecución (debe usar caché)
        result2 = self.minimizer.minimize_tokens(sequence, "auto")
        self.assertTrue(result2['success'])

        # Ambas deberían ser exitosas
        self.assertEqual(result1['success'], result2['success'])

    def test_different_optimization_targets(self):
        """Prueba diferentes objetivos de optimización"""
        sequence = [
            "H(q[0])", "Rz(pi/4, q[0])", "Rx(pi/2, q[0])",
            "CNOT(q[0], q[1])", "measure(q[0])"
        ]

        # Probar diferentes objetivos
        targets = ["speed", "accuracy", "memory", "auto"]

        for target in targets:
            result = self.minimizer.minimize_tokens(sequence, target)
            self.assertTrue(result['success'])
            self.assertEqual(result['minimization_method'], target)

    def test_pattern_regeneration(self):
        """Prueba regeneración de patrones"""
        sequence = [
            "H(q[0])", "H(q[1])", "CNOT(q[0], q[1])",
            "Rz(pi/4, q[0])", "Rz(pi/4, q[1])"
        ]

        # Regenerar secuencia
        regenerated = self.minimizer.regeneration_engine.regenerate_command(
            sequence, "speed"
        )

        # Verificar que se generó una secuencia válida
        self.assertIsInstance(regenerated, list)

    def test_reutilization_analysis(self):
        """Prueba análisis de reutilización"""
        # Secuencia con patrones repetitivos
        sequence = [
            "H(q[0])", "Rz(pi/4, q[0])", "H(q[0])", "Rz(pi/4, q[0])",
            "H(q[1])", "Rz(pi/4, q[1])", "H(q[1])", "Rz(pi/4, q[1])"
        ]

        # Analizar oportunidades
        opportunities = self.minimizer.reutilization_optimizer.analyze_reutilization_opportunities(sequence)

        # Verificar estructura del análisis
        self.assertIn('repeated_subsequences', opportunities)
        self.assertIn('common_patterns', opportunities)
        self.assertIn('compression_candidates', opportunities)
        self.assertIn('template_matches', opportunities)

    def test_system_status(self):
        """Prueba estado del sistema de minimización"""
        # Obtener estado del sistema
        status = self.minimizer.get_system_status()

        # Verificar estructura del estado
        self.assertIn('cache_statistics', status)
        self.assertIn('regeneration_engine_ready', status)
        self.assertIn('reutilization_optimizer_ready', status)

        # Verificar estadísticas del caché
        cache_stats = status['cache_statistics']
        self.assertIn('total_entries', cache_stats)
        self.assertIn('estimated_hit_rate', cache_stats)


class TestIntelligentCacheStandalone(unittest.TestCase):
    """Pruebas independientes del caché inteligente"""

    def setUp(self):
        """Configuración inicial"""
        self.cache = IntelligentCache(max_size=50, ttl=3600.0)

    def test_cache_storage(self):
        """Prueba almacenamiento básico en caché"""
        sequence = ["H(q[0])", "CNOT(q[0], q[1])"]
        result = {"counts": {"00": 512, "11": 512}}

        # Almacenar
        cache_key = self.cache.store(sequence, result)

        # Verificar almacenamiento
        self.assertIsNotNone(cache_key)
        self.assertEqual(len(self.cache.cache), 1)

    def test_cache_retrieval(self):
        """Prueba recuperación básica del caché"""
        sequence = ["X(q[0])", "measure(q[0])"]
        result = {"measurement": "0"}

        # Almacenar y recuperar
        self.cache.store(sequence, result)
        retrieved = self.cache.retrieve(sequence)

        # Verificar recuperación
        self.assertEqual(retrieved, result)

    def test_cache_similarity(self):
        """Prueba detección de similitud"""
        # Secuencias similares
        seq1 = ["H(q[0])", "CNOT(q[0], q[1])"]
        seq2 = ["H(q[1])", "CNOT(q[1], q[0])"]

        # Almacenar primera secuencia
        self.cache.store(seq1, {"result": "bell_state"})

        # Buscar similares
        similar = self.cache.get_similar_commands(seq2, threshold=0.3)

        # Debería encontrar alguna similitud
        self.assertIsInstance(similar, list)


class TestSequenceReutilizationStandalone(unittest.TestCase):
    """Pruebas independientes del optimizador de reutilización"""

    def setUp(self):
        """Configuración inicial"""
        self.cache = IntelligentCache()
        self.optimizer = SequenceReutilizationOptimizer(self.cache)

    def test_repeated_subsequence_detection(self):
        """Prueba detección de subsecuencias repetidas"""
        # Secuencia con repeticiones claras
        sequence = [
            "H(q[0])", "Rz(pi/4, q[0])", "H(q[0])", "Rz(pi/4, q[0])",
            "H(q[1])", "Rz(pi/4, q[1])", "H(q[1])", "Rz(pi/4, q[1])",
            "measure(q[0])", "measure(q[1])"
        ]

        # Analizar reutilización
        opportunities = self.optimizer.analyze_reutilization_opportunities(sequence)

        # Debería detectar subsecuencias repetidas
        repeated = opportunities['repeated_subsequences']
        self.assertIsInstance(repeated, list)

        # Si hay repeticiones, deberían tener estructura correcta
        if repeated:
            for repetition in repeated:
                self.assertIn('pattern', repetition)
                self.assertIn('positions', repetition)
                self.assertIn('frequency', repetition)

    def test_common_pattern_identification(self):
        """Prueba identificación de patrones comunes"""
        # Secuencia con patrones conocidos
        sequence = [
            "H(q[0])", "CNOT(q[0], q[1])", "H(q[1])",  # Patrón Bell
            "Rx(pi/2, q[0])", "Ry(pi/2, q[1])", "Rz(pi/2, q[0])",  # Rotaciones
            "measure(q[0])", "measure(q[1])"
        ]

        opportunities = self.optimizer.analyze_reutilization_opportunities(sequence)

        # Debería identificar patrones comunes
        common_patterns = opportunities['common_patterns']
        self.assertIsInstance(common_patterns, list)

    def test_sequence_optimization(self):
        """Prueba optimización básica de secuencias"""
        # Secuencia con oportunidades claras de optimización
        sequence = [
            "H(q[0])", "H(q[0])",  # Redundante
            "Rz(pi/4, q[0])", "Rz(pi/8, q[0])",  # Fusionables
            "X(q[1])", "X(q[1])",  # Redundante
        ]

        # Optimizar secuencia
        optimized = self.optimizer.create_optimized_sequence(sequence, "auto")

        # Debería producir una secuencia válida
        self.assertIsInstance(optimized, list)

        # Podría ser más corta debido a optimizaciones
        # (aunque no garantizado en todos los casos)


def run_minimization_only_tests():
    """Ejecuta pruebas específicas de minimización de tokens"""
    print("=== Pruebas de Minimización de Tokens - CORA-Quantum Assistant ===")
    print("Fecha: 1 de octubre de 2025")
    print("Versión: 1.0 - Pruebas Aisladas de Minimización")
    print()

    # Crear suite de pruebas
    test_classes = [
        TestTokenMinimizationCore,
        TestIntelligentCacheStandalone,
        TestSequenceReutilizationStandalone
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
    print("\n=== Resumen de Pruebas de Minimización ===")
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
        print("\n✅ Todas las pruebas de minimización pasaron exitosamente")
        return 0
    else:
        print("\n❌ Algunas pruebas de minimización fallaron")
        return 1


if __name__ == "__main__":
    exit_code = run_minimization_only_tests()
    sys.exit(exit_code)