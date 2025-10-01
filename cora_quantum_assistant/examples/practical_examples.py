#!/usr/bin/env python3
"""
Ejemplos de Uso Prácticos - CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import sys
import os
import numpy as np
import time

# Agregar directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.cora_quantum_assistant import CORAQuantumAssistant, QuantumConfig
from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator, SimulationConfig

class PracticalExamples:
    """Ejemplos prácticos de uso del CORA-Quantum Assistant"""

    def __init__(self):
        self.assistant = None
        self.simulator = None

    def initialize_system(self):
        """Inicializa el sistema para ejemplos"""
        print("🚀 Inicializando sistema para ejemplos prácticos...")

        # Configuración básica
        config = QuantumConfig(
            qubits=500,
            classical_bits=25,
            coherence_time=300.0,
            error_rate=1e-4
        )

        self.assistant = CORAQuantumAssistant(config)

        sim_config = SimulationConfig(
            max_qubits=500,
            classical_memory_limit=4 * 1024 * 1024 * 1024,  # 4GB
            hybrid_mode=True
        )

        self.simulator = HybridQuantumSimulator(sim_config)
        print("✓ Sistema inicializado")

    def example_portfolio_optimization(self):
        """Ejemplo 1: Optimización de portafolio financiero"""
        print("\n📈 EJEMPLO 1: Optimización de Portafolio Financiero")
        print("=" * 60)

        # Datos de mercado simulados
        n_assets = 20
        np.random.seed(42)

        # Rendimientos esperados (simulados)
        expected_returns = np.random.normal(0.08, 0.02, n_assets)

        # Matriz de covarianza (simulada)
        A = np.random.randn(n_assets, n_assets)
        covariance_matrix = np.dot(A, A.T) * 0.01

        print(f"Activos: {n_assets}")
        print(f"Rendimiento promedio: {expected_returns.mean():.2%}")
        print(f"Riesgo promedio: {np.sqrt(np.diag(covariance_matrix)).mean():.2%}")

        # Función de costo para optimización de portafolio
        def portfolio_cost(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))

            # Maximizar retorno, minimizar riesgo
            return -portfolio_return + 0.5 * portfolio_risk

        # Solución inicial (pesos iguales)
        initial_weights = np.ones(n_assets) / n_assets

        print("\nEjecutando optimización cuántica...")

        # Ejecutar optimización usando simulador híbrido
        start_time = time.time()
        result = self.simulator.simulate(portfolio_cost, initial_weights)
        optimization_time = time.time() - start_time

        print(f"Tiempo de optimización: {optimization_time:.3f}s")
        print(f"Modo usado: {result.mode_used}")
        print(f"Precisión: {result.accuracy*100:.1f}%")

        # Mostrar resultados
        optimal_weights = result.solution
        final_return = np.dot(optimal_weights, expected_returns)
        final_risk = np.sqrt(np.dot(optimal_weights.T, np.dot(covariance_matrix, optimal_weights)))

        print("\nResultados:")
        print(f"Rendimiento óptimo: {final_return:.2%}")
        print(f"Riesgo óptimo: {final_risk:.2%}")
        print(f"Ratio Sharpe: {final_return/final_risk:.3f}")

        # Mostrar distribución de pesos
        print("\nTop 5 activos por peso:")
        top_indices = np.argsort(optimal_weights)[-5:][::-1]
        for i, idx in enumerate(top_indices):
            print(f"  Activo {idx+1}: {optimal_weights[idx]:.1%}")

        return result

    def example_machine_learning_classification(self):
        """Ejemplo 2: Clasificación con Machine Learning cuántico"""
        print("\n🧠 EJEMPLO 2: Clasificación con Machine Learning Cuántico")
        print("=" * 60)

        # Generar datos sintéticos para clasificación
        np.random.seed(42)
        n_samples = 200
        n_features = 10

        # Crear dos clases con diferentes distribuciones
        class_0 = np.random.normal([2, 3] + [0]*8, 1, (n_samples//2, n_features))
        class_1 = np.random.normal([-2, -3] + [0]*8, 1, (n_samples//2, n_features))

        X = np.vstack([class_0, class_1])
        y = np.hstack([np.zeros(n_samples//2), np.ones(n_samples//2)])

        print(f"Datos de entrenamiento: {n_samples} muestras, {n_features} características")
        print(f"Clase 0: {n_samples//2} muestras")
        print(f"Clase 1: {n_samples//2} muestras")

        # Función de costo para clasificación cuántica
        def classification_cost(params):
            # Parámetros del modelo cuántico (simulado)
            weights = params[:n_features]
            bias = params[-1]

            # Predicciones lineales simples
            predictions = np.dot(X, weights) + bias

            # Función de pérdida (entropía cruzada simplificada)
            probabilities = 1 / (1 + np.exp(-predictions))
            loss = -np.mean(y * np.log(probabilities + 1e-8) + (1-y) * np.log(1-probabilities + 1e-8))

            return loss

        # Solución inicial
        initial_params = np.random.normal(0, 0.1, n_features + 1)

        print("\nEntrenando clasificador cuántico...")

        # Ejecutar optimización cuántica
        start_time = time.time()
        result = self.simulator.simulate(classification_cost, initial_params)
        training_time = time.time() - start_time

        print(f"Tiempo de entrenamiento: {training_time:.3f}s")
        print(f"Modo usado: {result.mode_used}")

        # Evaluar modelo
        optimal_params = result.solution
        optimal_weights = optimal_params[:n_features]
        optimal_bias = optimal_params[-1]

        # Predicciones en datos de entrenamiento
        train_predictions = np.dot(X, optimal_weights) + optimal_bias
        train_probabilities = 1 / (1 + np.exp(-train_predictions))
        train_predictions_binary = (train_probabilities > 0.5).astype(int)

        accuracy = np.mean(train_predictions_binary == y)

        print("\nResultados de entrenamiento:")
        print(f"Precisión en entrenamiento: {accuracy*100:.1f}%")
        print(f"Pérdida final: {classification_cost(optimal_params):.6f}")

        # Mostrar algunos pesos importantes
        print("\nCaracterísticas más importantes:")
        importance_indices = np.argsort(np.abs(optimal_weights))[-3:][::-1]
        for i, idx in enumerate(importance_indices):
            print(f"  Característica {idx+1}: {optimal_weights[idx]:.4f}")

        return result, accuracy

    def example_supply_chain_optimization(self):
        """Ejemplo 3: Optimización de cadena de suministro"""
        print("\n🏭 EJEMPLO 3: Optimización de Cadena de Suministro")
        print("=" * 60)

        # Parámetros del problema
        n_warehouses = 8
        n_customers = 15
        n_products = 5

        np.random.seed(42)

        # Costos de transporte (almacén -> cliente)
        transport_costs = np.random.uniform(10, 100, (n_warehouses, n_customers))

        # Capacidades de almacenes
        warehouse_capacity = np.random.uniform(1000, 5000, n_warehouses)

        # Demanda de clientes
        customer_demand = np.random.uniform(100, 800, (n_customers, n_products))

        print(f"Almacenes: {n_warehouses}")
        print(f"Clientes: {n_customers}")
        print(f"Productos: {n_products}")
        print(f"Capacidad promedio: {warehouse_capacity.mean():.0f} unidades")
        print(f"Demanda promedio: {customer_demand.mean():.0f} unidades")

        # Función de costo para optimización de cadena de suministro
        def supply_chain_cost(allocation_matrix):
            total_cost = 0

            # Costo de transporte
            for w in range(n_warehouses):
                for c in range(n_customers):
                    for p in range(n_products):
                        idx = w * n_customers * n_products + c * n_products + p
                        if idx < len(allocation_matrix):
                            quantity = allocation_matrix[idx]
                            total_cost += quantity * transport_costs[w, c]

            # Penalización por exceso de capacidad
            warehouse_usage = np.zeros(n_warehouses)
            for w in range(n_warehouses):
                for c in range(n_customers):
                    for p in range(n_products):
                        idx = w * n_customers * n_products + c * n_products + p
                        if idx < len(allocation_matrix):
                            warehouse_usage[w] += allocation_matrix[idx]

            capacity_penalty = np.sum(np.maximum(warehouse_usage - warehouse_capacity, 0) * 1000)
            total_cost += capacity_penalty

            return total_cost

        # Solución inicial (distribución uniforme)
        total_variables = n_warehouses * n_customers * n_products
        initial_solution = np.random.uniform(0, 10, total_variables)

        print("\nOptimizando cadena de suministro...")

        # Ejecutar optimización cuántica
        start_time = time.time()
        result = self.simulator.simulate(supply_chain_cost, initial_solution)
        optimization_time = time.time() - start_time

        print(f"Tiempo de optimización: {optimization_time:.3f}s")
        print(f"Modo usado: {result.mode_used}")

        # Analizar solución
        optimal_allocation = result.solution
        final_cost = supply_chain_cost(optimal_allocation)

        print("\nResultados:")
        print(f"Costo total óptimo: ${final_cost:,.0f}")

        # Análisis de uso de almacenes
        warehouse_usage = np.zeros(n_warehouses)
        for w in range(n_warehouses):
            for c in range(n_customers):
                for p in range(n_products):
                    idx = w * n_customers * n_products + c * n_products + p
                    if idx < len(optimal_allocation):
                        warehouse_usage[w] += optimal_allocation[idx]

        print("\nUso de almacenes:")
        for w in range(n_warehouses):
            usage_pct = (warehouse_usage[w] / warehouse_capacity[w]) * 100
            print(f"  Almacén {w+1}: {usage_pct:.1f}% capacidad")

        return result

    def example_drug_discovery_optimization(self):
        """Ejemplo 4: Optimización de descubrimiento de fármacos"""
        print("\n💊 EJEMPLO 4: Optimización de Descubrimiento de Fármacos")
        print("=" * 60)

        # Parámetros moleculares simulados
        n_molecules = 50
        n_properties = 8

        np.random.seed(42)

        # Propiedades moleculares (eficacia, toxicidad, solubilidad, etc.)
        molecular_properties = np.random.uniform(0, 1, (n_molecules, n_properties))

        # Pesos de importancia para cada propiedad
        property_weights = np.array([2.0, -1.5, 1.0, 0.8, -0.5, 1.2, 0.3, -0.8])

        print(f"Moléculas candidatas: {n_molecules}")
        print(f"Propiedades evaluadas: {n_properties}")
        print(f"Propiedad promedio: {molecular_properties.mean():.3f}")

        # Función de costo para optimización de fármacos
        def drug_cost(molecule_params):
            # molecule_params representa parámetros de optimización adicionales
            base_score = np.dot(molecular_properties, property_weights)

            # Agregar efecto de parámetros de optimización
            optimization_bonus = np.sum(molecule_params ** 2) * 0.1

            return -np.sum(base_score) + optimization_bonus

        # Solución inicial
        initial_params = np.random.normal(0, 0.1, 10)

        print("\nOptimizando descubrimiento de fármacos...")

        # Ejecutar optimización cuántica
        start_time = time.time()
        result = self.simulator.simulate(drug_cost, initial_params)
        optimization_time = time.time() - start_time

        print(f"Tiempo de optimización: {optimization_time:.3f}s")
        print(f"Modo usado: {result.mode_used}")

        # Evaluar moléculas candidatas
        scores = -np.dot(molecular_properties, property_weights)  # Negativo porque minimizamos costo

        print("\nAnálisis de moléculas:")
        print(f"Puntuación promedio: {scores.mean():.3f}")
        print(f"Mejor puntuación: {scores.min():.3f}")
        print(f"Peor puntuación: {scores.max():.3f}")

        # Identificar mejores candidatos
        best_indices = np.argsort(scores)[:5]
        print("\nTop 5 candidatos:")
        for i, idx in enumerate(best_indices):
            print(f"  Molécula {idx+1}: puntuación {scores[idx]:.3f}")

        return result

    def example_quantum_chemistry_simulation(self):
        """Ejemplo 5: Simulación química cuántica"""
        print("\n⚗️  EJEMPLO 5: Simulación Química Cuántica")
        print("=" * 60)

        # Simulación básica de molécula H2
        print("Simulando molécula de hidrógeno (H₂)...")

        # Función de costo representando energía molecular
        def molecular_energy(params):
            # Parámetros: distancia internuclear, ángulos, etc.
            distance = params[0]
            angle = params[1]

            # Energía potencial (simplificada)
            h2_energy = 1/distance**12 - 2/distance**6  # Potencial Lennard-Jones

            # Agregar términos angulares
            angular_term = np.sin(angle)**2

            return h2_energy + angular_term

        # Rango de distancias internucleares típico para H2
        initial_distance = 0.74  # Angstroms
        initial_angle = 0.0

        initial_params = np.array([initial_distance, initial_angle])

        print(f"Distancia inicial: {initial_distance} Å")
        print(f"Energía inicial: {molecular_energy(initial_params):.6f} Hartree")

        # Ejecutar simulación cuántica
        start_time = time.time()
        result = self.simulator.simulate(molecular_energy, initial_params)
        simulation_time = time.time() - start_time

        print(f"Tiempo de simulación: {simulation_time:.3f}s")
        print(f"Modo usado: {result.mode_used}")

        # Analizar resultado
        optimal_distance = result.solution[0]
        optimal_angle = result.solution[1]
        final_energy = molecular_energy(result.solution)

        print("\nResultados de simulación:")
        print(f"Distancia óptima: {optimal_distance:.3f} Å")
        print(f"Ángulo óptimo: {optimal_angle:.3f} rad")
        print(f"Energía final: {final_energy:.6f} Hartree")
        print(f"Cambio de energía: {final_energy - molecular_energy(initial_params):.6f} Hartree")

        return result

    def run_all_examples(self):
        """Ejecuta todos los ejemplos prácticos"""
        print("🚀 EJEMPLOS PRÁCTICOS - CORA-Quantum Assistant")
        print("=" * 80)
        print("Demostración de aplicaciones reales del asistente cuántico")
        print("=" * 80)

        # Inicializar sistema
        self.initialize_system()

        # Ejecutar ejemplos
        examples = [
            ("Optimización de Portafolio", self.example_portfolio_optimization),
            ("Clasificación ML Cuántico", self.example_machine_learning_classification),
            ("Optimización Cadena Suministro", self.example_supply_chain_optimization),
            ("Descubrimiento de Fármacos", self.example_drug_discovery_optimization),
            ("Simulación Química", self.example_quantum_chemistry_simulation)
        ]

        results = {}

        for name, example_func in examples:
            try:
                print(f"\n{'='*80}")
                result = example_func()
                results[name] = {'status': 'success', 'result': result}
                print(f"✓ {name} completado exitosamente")

            except Exception as e:
                print(f"✗ Error en {name}: {str(e)}")
                results[name] = {'status': 'error', 'error': str(e)}

        # Resumen final
        print(f"\n{'='*80}")
        print("📊 RESUMEN DE EJEMPLOS PRÁCTICOS")
        print("=" * 80)

        successful = sum(1 for r in results.values() if r['status'] == 'success')
        total = len(results)

        print(f"Ejemplos exitosos: {successful}/{total}")

        for name, result in results.items():
            status_icon = "✓" if result['status'] == 'success' else "✗"
            print(f"  {status_icon} {name}")

        print("\n🎉 Demostración de ejemplos prácticos completada!")
        print("=" * 80)

        return results

def main():
    """Función principal"""
    examples = PracticalExamples()
    examples.run_all_examples()

if __name__ == "__main__":
    main()