#!/usr/bin/env python3
"""
Configuración Básica del Entorno - CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class QuantumEnvironmentConfig:
    """Configuración completa del entorno cuántico"""

    # Configuración básica del sistema
    system_name: str = "CORA-Quantum Assistant"
    version: str = "1.0"
    debug_mode: bool = False

    # Configuración cuántica
    qubits: int = 1000
    classical_bits: int = 50
    coherence_time: float = 500.0  # microsegundos
    error_rate: float = 1e-4
    connectivity: str = "all-to-all"

    # Configuración del simulador híbrido
    max_qubits_simulation: int = 1000
    classical_memory_limit: int = 8 * 1024 * 1024 * 1024  # 8GB
    quantum_error_rate: float = 1e-4
    classical_threshold: int = 100  # Problemas menores usan modo clásico
    hybrid_mode: bool = True
    noise_simulation: bool = True

    # Configuración de minimización de tokens
    token_cache_size: int = 1000
    cache_ttl: float = 3600.0  # 1 hora
    enable_token_minimization: bool = True
    enable_physics_integration: bool = True

    # Configuración de logging
    log_level: str = "INFO"
    log_file: str = "cora_quantum.log"
    enable_console_logging: bool = True

    # Configuración de archivos
    base_directory: str = ""
    config_file: str = "config.json"
    data_directory: str = "data"
    logs_directory: str = "logs"
    examples_directory: str = "examples"

    # Configuración de rendimiento
    max_concurrent_tasks: int = 5
    timeout_quantum_tasks: float = 300.0  # 5 minutos
    enable_parallel_processing: bool = True

class EnvironmentConfigurator:
    """Configurador del entorno CORA-Quantum"""

    def __init__(self, config_file: str = None):
        self.config_file = config_file or "config.json"
        self.config_directory = Path(__file__).parent
        self.config_path = self.config_directory / self.config_file
        self.config = QuantumEnvironmentConfig()

    def create_default_config(self) -> QuantumEnvironmentConfig:
        """Crea configuración por defecto"""
        print("🔧 Creando configuración por defecto del entorno...")

        # Detectar recursos del sistema automáticamente
        self._auto_detect_resources()

        # Crear directorios necesarios
        self._create_directories()

        # Guardar configuración
        self.save_config()

        print(f"✓ Configuración creada en: {self.config_path}")
        return self.config

    def _auto_detect_resources(self):
        """Detecta automáticamente recursos del sistema"""
        try:
            import psutil
            import multiprocessing

            # Detectar memoria disponible
            memory_gb = psutil.virtual_memory().available / (1024**3)
            self.config.classical_memory_limit = int(memory_gb * 1024 * 1024 * 1024 * 0.8)  # 80% de memoria disponible

            # Detectar CPUs
            cpu_count = multiprocessing.cpu_count()
            self.config.max_concurrent_tasks = min(cpu_count, 10)

            # Ajustar qubits según memoria disponible
            if memory_gb > 16:
                self.config.qubits = 2000
                self.config.max_qubits_simulation = 2000
            elif memory_gb > 8:
                self.config.qubits = 1000
                self.config.max_qubits_simulation = 1000
            else:
                self.config.qubits = 500
                self.config.max_qubits_simulation = 500

            print(f"  Recursos detectados: {memory_gb:.1f}GB RAM, {cpu_count} CPUs")
            print(f"  Configuración ajustada: {self.config.qubits} qubits, límite memoria: {memory_gb*0.8:.1f}GB")

        except ImportError:
            print("  Advertencia: psutil no disponible, usando configuración por defecto")
        except Exception as e:
            print(f"  Error detectando recursos: {e}")

    def _create_directories(self):
        """Crea directorios necesarios"""
        directories = [
            self.config.data_directory,
            self.config.logs_directory,
            self.config.examples_directory,
            "temp",
            "output"
        ]

        for directory in directories:
            dir_path = self.config_directory / directory
            dir_path.mkdir(exist_ok=True)
            print(f"  ✓ Directorio creado: {directory}")

    def load_config(self) -> QuantumEnvironmentConfig:
        """Carga configuración desde archivo"""
        if not self.config_path.exists():
            print(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
            return self.create_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Actualizar configuración con datos del archivo
            for key, value in data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

            print(f"✓ Configuración cargada desde: {self.config_path}")
            return self.config

        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            print("Usando configuración por defecto...")
            return self.create_default_config()

    def save_config(self):
        """Guarda configuración en archivo"""
        try:
            # Crear directorio si no existe
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Convertir configuración a diccionario
            config_dict = asdict(self.config)

            # Agregar metadatos
            config_dict['_metadata'] = {
                'created_at': self._get_timestamp(),
                'version': self.config.version,
                'auto_detected': True
            }

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)

            print(f"✓ Configuración guardada en: {self.config_path}")

        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")

    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()

    def validate_config(self) -> bool:
        """Valida configuración actual"""
        print("🔍 Validando configuración...")

        issues = []

        # Validar parámetros cuánticos
        if self.config.qubits <= 0:
            issues.append("Número de qubits debe ser positivo")
        if self.config.coherence_time <= 0:
            issues.append("Tiempo de coherencia debe ser positivo")
        if self.config.error_rate < 0 or self.config.error_rate > 1:
            issues.append("Tasa de error debe estar entre 0 y 1")

        # Validar configuración del simulador
        if self.config.max_qubits_simulation > self.config.qubits:
            issues.append("Máximo de qubits de simulación no puede exceder qubits totales")

        # Validar memoria
        if self.config.classical_memory_limit <= 0:
            issues.append("Límite de memoria debe ser positivo")

        # Validar configuración de minimización de tokens
        if self.config.token_cache_size <= 0:
            issues.append("Tamaño de caché de tokens debe ser positivo")

        if issues:
            print("❌ Problemas encontrados en la configuración:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("✓ Configuración válida")
            return True

    def show_config_summary(self):
        """Muestra resumen de configuración"""
        print("\n📋 Resumen de Configuración:")
        print("=" * 50)
        print(f"Sistema: {self.config.system_name} v{self.config.version}")
        print(f"Qubits: {self.config.qubits}")
        print(f"Bits clásicos: {self.config.classical_bits}")
        print(f"Tiempo de coherencia: {self.config.coherence_time} μs")
        print(f"Tasa de error: {self.config.error_rate}")
        print(f"Modo híbrido: {'Activado' if self.config.hybrid_mode else 'Desactivado'}")
        print(f"Minimización de tokens: {'Activada' if self.config.enable_token_minimization else 'Desactivada'}")
        print(f"Integración física: {'Activada' if self.config.enable_physics_integration else 'Desactivada'}")
        print(f"Límite de memoria: {self.config.classical_memory_limit / (1024**3):.1f} GB")
        print(f"Tareas concurrentes: {self.config.max_concurrent_tasks}")
        print(f"Nivel de log: {self.config.log_level}")

    def get_config_for_component(self, component: str) -> Dict[str, Any]:
        """Obtiene configuración específica para un componente"""
        if component == 'quantum_assistant':
            return {
                'qubits': self.config.qubits,
                'classical_bits': self.config.classical_bits,
                'coherence_time': self.config.coherence_time,
                'error_rate': self.config.error_rate,
                'connectivity': self.config.connectivity
            }
        elif component == 'hybrid_simulator':
            return {
                'max_qubits': self.config.max_qubits_simulation,
                'classical_memory_limit': self.config.classical_memory_limit,
                'quantum_error_rate': self.config.quantum_error_rate,
                'classical_threshold': self.config.classical_threshold,
                'hybrid_mode': self.config.hybrid_mode,
                'noise_simulation': self.config.noise_simulation
            }
        elif component == 'token_minimizer':
            return {
                'cache_size': self.config.token_cache_size,
                'cache_ttl': self.config.cache_ttl,
                'enabled': self.config.enable_token_minimization
            }
        else:
            return {}

def setup_environment():
    """Función principal de configuración del entorno"""
    print("🌟 Configuración del Entorno CORA-Quantum Assistant")
    print("=" * 60)

    configurator = EnvironmentConfigurator()

    # Cargar configuración existente o crear nueva
    config = configurator.load_config()

    # Mostrar resumen de configuración
    configurator.show_config_summary()

    # Validar configuración
    if not configurator.validate_config():
        print("\n⚠️  Configuración inválida. ¿Desea crear una nueva configuración? (y/n)")
        response = input().lower().strip()
        if response == 'y' or response == 'yes':
            config = configurator.create_default_config()
        else:
            print("Usando configuración actual con problemas conocidos...")

    print("\n✅ Entorno configurado exitosamente")
    return configurator

def get_environment_info() -> Dict[str, Any]:
    """Obtiene información del entorno del sistema"""
    info = {
        'platform': 'unknown',
        'python_version': 'unknown',
        'memory_available': 0,
        'cpu_count': 0,
        'dependencies_available': {}
    }

    try:
        import platform
        info['platform'] = platform.platform()
        info['python_version'] = platform.python_version()

        import psutil
        info['memory_available'] = psutil.virtual_memory().available
        info['cpu_count'] = psutil.cpu_count()

        # Verificar dependencias críticas
        dependencies = ['numpy', 'scipy', 'qiskit', 'matplotlib']
        for dep in dependencies:
            try:
                __import__(dep)
                info['dependencies_available'][dep] = True
            except ImportError:
                info['dependencies_available'][dep] = False

    except ImportError:
        pass  # psutil no disponible
    except Exception as e:
        logger.warning(f"Error obteniendo información del entorno: {e}")

    return info

if __name__ == "__main__":
    # Ejecutar configuración cuando se ejecuta directamente
    configurator = setup_environment()

    # Mostrar información del entorno
    print("\n🔍 Información del Entorno del Sistema:")
    print("-" * 40)
    env_info = get_environment_info()

    print(f"Plataforma: {env_info['platform']}")
    print(f"Python: {env_info['python_version']}")
    print(f"Memoria disponible: {env_info['memory_available'] / (1024**3):.1f} GB")
    print(f"CPUs: {env_info['cpu_count']}")

    print("\nDependencias disponibles:")
    for dep, available in env_info['dependencies_available'].items():
        status = "✓" if available else "✗"
        print(f"  {status} {dep}")

    print("\n🎯 Configuración del entorno completada!")
    print("Puede ejecutar 'python main.py' para iniciar CORA-Quantum Assistant")