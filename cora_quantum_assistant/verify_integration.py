#!/usr/bin/env python3
"""
Verificación de Integración de Componentes - CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import sys
import os
import importlib.util
import time
from typing import Dict, List, Any
import logging

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegrationVerifier:
    """Verificador de integración de componentes"""

    def __init__(self):
        self.components = {
            'core': {
                'module': 'core.cora_quantum_assistant',
                'class': 'CORAQuantumAssistant',
                'required': True
            },
            'hybrid_simulator': {
                'module': 'hybrid_simulator.hybrid_quantum_simulator',
                'class': 'HybridQuantumSimulator',
                'required': True
            },
            'token_minimizer': {
                'module': 'core.token_minimization',
                'class': 'TokenMinimizationManager',
                'required': True
            },
            'physics_integrator': {
                'module': 'core.physics_integration',
                'class': 'TokenPhysicsIntegrator',
                'required': True
            },
            'quantum_omega_examples': {
                'module': 'quantum_omega_language.examples',
                'class': None,  # Solo verificar que existe el archivo
                'required': True
            }
        }

        self.integration_results = {}

    def verify_all_components(self) -> Dict[str, Any]:
        """Verifica todos los componentes"""
        print("🔍 Verificando integración de componentes...")
        print("=" * 60)

        all_passed = True

        for component_name, component_info in self.components.items():
            print(f"\n📦 Verificando componente: {component_name}")

            result = self.verify_component(component_name, component_info)
            self.integration_results[component_name] = result

            if result['status'] == 'success':
                print(f"   ✓ {component_name} integrado correctamente")
            else:
                print(f"   ✗ Error en {component_name}: {result['error']}")
                if component_info['required']:
                    all_passed = False

        print("\n" + "=" * 60)

        if all_passed:
            print("🎉 Todos los componentes esenciales están integrados correctamente")
        else:
            print("⚠️  Algunos componentes tienen problemas de integración")

        return {
            'all_passed': all_passed,
            'results': self.integration_results,
            'summary': self._generate_summary()
        }

    def verify_component(self, name: str, component_info: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica un componente específico"""
        try:
            # Verificar importación del módulo
            module_path = component_info['module']
            module = self._import_module(module_path)

            if module is None:
                return {
                    'status': 'error',
                    'error': f'No se pudo importar el módulo {module_path}',
                    'details': 'Archivo o módulo no encontrado'
                }

            # Si se especifica una clase, verificar que existe
            if component_info['class']:
                class_name = component_info['class']
                if not hasattr(module, class_name):
                    return {
                        'status': 'error',
                        'error': f'Clase {class_name} no encontrada en {module_path}',
                        'details': f'Atributos disponibles: {list(dir(module))}'
                    }

                # Intentar instanciar la clase para verificar que funciona
                try:
                    cls = getattr(module, class_name)
                    if name == 'core':
                        # Para CORAQuantumAssistant necesitamos configuración especial
                        instance = cls()
                    elif name == 'hybrid_simulator':
                        # Para HybridQuantumSimulator
                        instance = cls()
                    elif name == 'token_minimizer':
                        # Para TokenMinimizationManager
                        instance = cls(cache_size=100, cache_ttl=3600.0)
                    elif name == 'physics_integrator':
                        # Para TokenPhysicsIntegrator
                        instance = cls()
                    else:
                        instance = cls()

                    # Verificar que la instancia tiene métodos básicos
                    if hasattr(instance, '__init__'):
                        pass  # Ya se instanció correctamente

                except Exception as e:
                    return {
                        'status': 'error',
                        'error': f'Error instanciando {class_name}: {str(e)}',
                        'details': 'Problema en el constructor de la clase'
                    }

            return {
                'status': 'success',
                'module': module_path,
                'class': component_info['class'],
                'details': 'Componente verificado correctamente'
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'details': 'Error inesperado durante verificación'
            }

    def _import_module(self, module_path: str):
        """Importa un módulo dado su path"""
        try:
            # Convertir path de módulo a path de archivo
            file_path = module_path.replace('.', '/') + '.py'
            full_path = os.path.join(os.path.dirname(__file__), file_path)

            if not os.path.exists(full_path):
                return None

            # Cargar módulo desde archivo
            spec = importlib.util.spec_from_file_location(module_path, full_path)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return module

        except Exception as e:
            logger.error(f"Error importando módulo {module_path}: {e}")
            return None

    def _generate_summary(self) -> Dict[str, Any]:
        """Genera resumen de verificación"""
        total_components = len(self.components)
        successful_components = sum(1 for r in self.integration_results.values() if r['status'] == 'success')
        failed_components = total_components - successful_components

        required_components = sum(1 for c in self.components.values() if c['required'])
        successful_required = sum(1 for name, result in self.integration_results.items()
                                if result['status'] == 'success' and self.components[name]['required'])

        return {
            'total_components': total_components,
            'successful_components': successful_components,
            'failed_components': failed_components,
            'required_components': required_components,
            'successful_required': successful_required,
            'system_ready': failed_components == 0 or successful_required == required_components
        }

    def test_basic_functionality(self) -> Dict[str, Any]:
        """Prueba funcionalidad básica de componentes integrados"""
        print("\n🧪 Probando funcionalidad básica de componentes...")
        print("-" * 50)

        functionality_results = {}

        try:
            # Probar asistente cuántico básico
            print("Probando CORA-Quantum Assistant...")
            from core.cora_quantum_assistant import CORAQuantumAssistant, QuantumConfig

            config = QuantumConfig(qubits=100, classical_bits=10)
            assistant = CORAQuantumAssistant(config)

            # Verificar estado del sistema
            status = assistant.get_system_status()
            if status['quantum_processor_ready']:
                print("   ✓ Asistente cuántico funcional")
                functionality_results['quantum_assistant'] = 'success'
            else:
                print("   ✗ Asistente cuántico no funcional")
                functionality_results['quantum_assistant'] = 'error'

        except Exception as e:
            print(f"   ✗ Error en asistente cuántico: {e}")
            functionality_results['quantum_assistant'] = f'error: {str(e)}'

        try:
            # Probar simulador híbrido básico
            print("Probando simulador híbrido...")
            from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator

            simulator = HybridQuantumSimulator()

            # Función de costo simple
            def simple_cost(x):
                return sum(x**2)

            initial_solution = [1.0, 2.0, 3.0]
            result = simulator.simulate(simple_cost, initial_solution)

            if result.solution is not None:
                print("   ✓ Simulador híbrido funcional")
                functionality_results['hybrid_simulator'] = 'success'
            else:
                print("   ✗ Simulador híbrido no funcional")
                functionality_results['hybrid_simulator'] = 'error'

        except Exception as e:
            print(f"   ✗ Error en simulador híbrido: {e}")
            functionality_results['hybrid_simulator'] = f'error: {str(e)}'

        try:
            # Probar minimización de tokens básica
            print("Probando minimización de tokens...")
            from core.token_minimization import TokenMinimizationManager

            minimizer = TokenMinimizationManager(cache_size=100, cache_ttl=3600.0)

            test_sequence = ["H(q[0])", "H(q[1])", "CNOT(q[0], q[1])", "H(q[0])", "H(q[1])"]
            result = minimizer.minimize_tokens(test_sequence, "auto")

            if result['success']:
                print("   ✓ Minimización de tokens funcional")
                functionality_results['token_minimizer'] = 'success'
            else:
                print("   ✗ Minimización de tokens no funcional")
                functionality_results['token_minimizer'] = 'error'

        except Exception as e:
            print(f"   ✗ Error en minimización de tokens: {e}")
            functionality_results['token_minimizer'] = f'error: {str(e)}'

        return functionality_results

    def generate_integration_report(self) -> str:
        """Genera reporte completo de integración"""
        summary = self._generate_summary()

        report = []
        report.append("📋 REPORTE DE INTEGRACIÓN DE COMPONENTES")
        report.append("=" * 60)
        report.append(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Versión: 1.0 - Prototipo Inicial")
        report.append("")

        report.append("RESUMEN EJECUTIVO:")
        report.append("-" * 30)
        report.append(f"✓ Componentes exitosos: {summary['successful_components']}/{summary['total_components']}")
        report.append(f"✗ Componentes fallidos: {summary['failed_components']}/{summary['total_components']}")
        report.append(f"✓ Componentes requeridos: {summary['successful_required']}/{summary['required_components']}")
        report.append(f"📊 Sistema listo: {'Sí' if summary['system_ready'] else 'No'}")
        report.append("")

        report.append("DETALLE DE COMPONENTES:")
        report.append("-" * 30)
        for component_name, result in self.integration_results.items():
            status_icon = "✓" if result['status'] == 'success' else "✗"
            required_icon = "(*)" if self.components[component_name]['required'] else ""

            report.append(f"{status_icon} {component_name}{required_icon}")
            if result['status'] != 'success':
                report.append(f"    Error: {result['error']}")
            else:
                report.append(f"    OK: {result['details']}")

        report.append("")
        report.append("PRUEBA DE FUNCIONALIDAD:")
        report.append("-" * 30)

        func_results = self.test_basic_functionality()
        for component, status in func_results.items():
            status_icon = "✓" if status == 'success' else "✗"
            report.append(f"{status_icon} {component}: {status}")

        report.append("")
        report.append("=" * 60)
        if summary['system_ready']:
            report.append("🎉 SISTEMA LISTO PARA USO")
        else:
            report.append("⚠️  SISTEMA REQUIERE ATENCIÓN")

        return "\n".join(report)

def main():
    """Función principal de verificación"""
    print("🚀 CORA-Quantum Assistant - Verificación de Integración")
    print("=" * 60)

    verifier = IntegrationVerifier()

    # Verificar componentes
    integration_result = verifier.verify_all_components()

    # Generar y mostrar reporte
    report = verifier.generate_integration_report()
    print(report)

    # Guardar reporte en archivo
    try:
        with open('integration_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("\n💾 Reporte guardado en: integration_report.txt")
    except Exception as e:
        print(f"\n❌ Error guardando reporte: {e}")

    # Código de salida basado en resultado
    if integration_result['all_passed']:
        print("\n✅ Verificación completada exitosamente")
        return 0
    else:
        print("\n❌ Verificación completada con errores")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)