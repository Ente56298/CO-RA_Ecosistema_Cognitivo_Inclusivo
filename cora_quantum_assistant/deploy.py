#!/usr/bin/env python3
"""
Script de Despliegue Automatizado - CORA-Quantum Assistant
Fecha: 1 de octubre de 2025
Versión: 1.0 - Prototipo Inicial
"""

import sys
import os
import subprocess
import shutil
import time
import platform
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentManager:
    """Gestor de despliegue automatizado"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.venv_name = "cora_quantum_env"
        self.venv_path = self.project_root / self.venv_name

    def check_system_requirements(self) -> Dict[str, Any]:
        """Verifica requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        requirements = {}

        # Verificar Python
        python_version = platform.python_version()
        requirements['python_version'] = python_version
        requirements['python_ok'] = sys.version_info >= (3, 8)

        # Verificar memoria
        try:
            import psutil
            memory_gb = psutil.virtual_memory().available / (1024**3)
            requirements['memory_gb'] = memory_gb
            requirements['memory_ok'] = memory_gb >= 4  # 4GB mínimo
        except ImportError:
            requirements['memory_ok'] = True  # Asumir OK si no se puede verificar

        # Verificar espacio en disco
        disk_usage = shutil.disk_usage(self.project_root)
        disk_gb = disk_usage.free / (1024**3)
        requirements['disk_gb'] = disk_gb
        requirements['disk_ok'] = disk_gb >= 2  # 2GB mínimo

        # Mostrar resultados
        print(f"  Python: {python_version} {'✓' if requirements['python_ok'] else '✗'}")
        print(f"  Memoria: {requirements.get('memory_gb', 0):.1f}GB {'✓' if requirements.get('memory_ok', True) else '✗'}")
        print(f"  Disco: {disk_gb:.1f}GB {'✓' if requirements['disk_ok'] else '✗'}")

        return requirements

    def create_virtual_environment(self) -> bool:
        """Crea entorno virtual"""
        print("🐍 Creando entorno virtual...")

        try:
            # Crear entorno virtual
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)],
                         check=True, capture_output=True)

            print(f"✓ Entorno virtual creado: {self.venv_path}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"✗ Error creando entorno virtual: {e}")
            return False
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
            return False

    def install_dependencies(self) -> bool:
        """Instala dependencias"""
        print("📦 Instalando dependencias...")

        try:
            # Activar entorno virtual y instalar dependencias
            if platform.system() == "Windows":
                pip_cmd = str(self.venv_path / "Scripts" / "pip.exe")
                python_cmd = str(self.venv_path / "Scripts" / "python.exe")
            else:
                pip_cmd = str(self.venv_path / "bin" / "pip")
                python_cmd = str(self.venv_path / "bin" / "python")

            # Actualizar pip
            subprocess.run([pip_cmd, "install", "--upgrade", "pip"],
                         check=True, capture_output=True)

            # Instalar dependencias desde requirements.txt
            if self.requirements_file.exists():
                subprocess.run([pip_cmd, "install", "-r", str(self.requirements_file)],
                             check=True, capture_output=True)
                print("✓ Dependencias instaladas desde requirements.txt")
            else:
                # Instalar dependencias básicas manualmente
                basic_deps = [
                    "numpy", "scipy", "matplotlib", "qiskit", "qiskit-aer",
                    "scikit-learn", "pytest", "pyyaml"
                ]
                subprocess.run([pip_cmd, "install"] + basic_deps,
                             check=True, capture_output=True)
                print("✓ Dependencias básicas instaladas")

            # Verificar instalación
            result = subprocess.run([python_cmd, "-c", "import qiskit; print('Qiskit OK')"],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Verificación de instalación exitosa")
                return True
            else:
                print(f"✗ Error en verificación: {result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"✗ Error instalando dependencias: {e}")
            return False
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
            return False

    def run_basic_tests(self) -> bool:
        """Ejecuta pruebas básicas"""
        print("🧪 Ejecutando pruebas básicas...")

        try:
            if platform.system() == "Windows":
                python_cmd = str(self.venv_path / "Scripts" / "python.exe")
            else:
                python_cmd = str(self.venv_path / "bin" / "python")

            # Ejecutar pruebas básicas
            test_files = [
                "test_cora_basic.py",
                "test_comprehensive.py"
            ]

            all_passed = True

            for test_file in test_files:
                test_path = self.project_root / test_file
                if test_path.exists():
                    print(f"  Ejecutando {test_file}...")
                    result = subprocess.run([python_cmd, str(test_path)],
                                          capture_output=True, text=True, timeout=300)

                    if result.returncode == 0:
                        print(f"  ✓ {test_file} pasó")
                    else:
                        print(f"  ⚠️  {test_file} tuvo problemas")
                        print(f"    Salida: {result.stdout[-500:]}")  # Últimas 500 líneas
                        if result.stderr:
                            print(f"    Error: {result.stderr[-500:]}")
                        all_passed = False

            return all_passed

        except subprocess.TimeoutExpired:
            print("✗ Pruebas excedieron tiempo límite")
            return False
        except Exception as e:
            print(f"✗ Error ejecutando pruebas: {e}")
            return False

    def create_startup_scripts(self) -> bool:
        """Crea scripts de inicio"""
        print("🚀 Creando scripts de inicio...")

        try:
            # Script de inicio principal
            startup_script = self._create_main_startup_script()
            startup_path = self.project_root / "start_cora_quantum.bat" if platform.system() == "Windows" else self.project_root / "start_cora_quantum.sh"

            with open(startup_path, 'w', encoding='utf-8') as f:
                f.write(startup_script)

            if platform.system() != "Windows":
                os.chmod(startup_path, 0o755)  # Hacer ejecutable en Unix

            print(f"✓ Script de inicio creado: {startup_path}")

            # Crear script de configuración rápida
            config_script = self._create_config_script()
            config_path = self.project_root / "configure.py"

            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_script)

            print(f"✓ Script de configuración creado: {config_path}")

            return True

        except Exception as e:
            print(f"✗ Error creando scripts de inicio: {e}")
            return False

    def _create_main_startup_script(self) -> str:
        """Crea script de inicio principal"""
        if platform.system() == "Windows":
            return f'''@echo off
echo "🚀 Iniciando CORA-Quantum Assistant..."
echo "Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}"
echo "Versión: 1.0 - Prototipo Inicial"
echo.

REM Activar entorno virtual
echo "🐍 Activando entorno virtual..."
call "{self.venv_path / "Scripts" / "activate.bat"}"

REM Verificar activación
python -c "import sys; print(f'Python: {{sys.executable}}')"

REM Ejecutar aplicación principal
echo.
echo "🎯 Iniciando aplicación..."
python main.py --mode interactive

pause
'''
        else:
            return f'''#!/bin/bash
echo "🚀 Iniciando CORA-Quantum Assistant..."
echo "Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}"
echo "Versión: 1.0 - Prototipo Inicial"
echo

# Activar entorno virtual
echo "🐍 Activando entorno virtual..."
source "{self.venv_path / "bin" / "activate"}"

# Verificar activación
python3 -c "import sys; print(f'Python: {{sys.executable}}')"

# Ejecutar aplicación principal
echo
echo "🎯 Iniciando aplicación..."
python3 main.py --mode interactive
'''

    def _create_config_script(self) -> str:
        """Crea script de configuración rápida"""
        return '''#!/usr/bin/env python3
"""
Script de Configuración Rápida - CORA-Quantum Assistant
"""

import sys
import os

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("⚙️  Configuración Rápida - CORA-Quantum Assistant")
    print("=" * 50)

    try:
        # Ejecutar configuración
        from config import setup_environment

        configurator = setup_environment()

        print("\\n✅ Configuración completada exitosamente!")
        print("\\nPara iniciar el sistema, ejecute:")
        print("  python main.py    (modo interactivo)")
        print("  python main.py --mode demo    (demostración)")

    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
'''

    def create_deployment_package(self) -> bool:
        """Crea paquete de despliegue"""
        print("📦 Creando paquete de despliegue...")

        try:
            # Crear directorio de distribución
            dist_dir = self.project_root / "dist"
            dist_dir.mkdir(exist_ok=True)

            # Archivos esenciales para el despliegue
            essential_files = [
                "main.py",
                "config.py",
                "verify_integration.py",
                "requirements.txt",
                "README.md",
                "core/",
                "hybrid_simulator/",
                "quantum_omega_language/",
                "examples/",
                "docs/"
            ]

            # Copiar archivos esenciales
            for file_item in essential_files:
                src_path = self.project_root / file_item
                if src_path.exists():
                    if src_path.is_file():
                        shutil.copy2(src_path, dist_dir / file_item)
                    else:
                        dst_path = dist_dir / file_item
                        if dst_path.exists():
                            shutil.rmtree(dst_path)
                        shutil.copytree(src_path, dst_path)

            # Crear script de instalación para el paquete
            install_script = self._create_install_script()
            if platform.system() == "Windows":
                install_path = dist_dir / "install.bat"
            else:
                install_path = dist_dir / "install.sh"

            with open(install_path, 'w', encoding='utf-8') as f:
                f.write(install_script)

            if platform.system() != "Windows":
                os.chmod(install_path, 0o755)

            print(f"✓ Paquete de despliegue creado: {dist_dir}")
            print(f"✓ Script de instalación: {install_path}")

            return True

        except Exception as e:
            print(f"✗ Error creando paquete de despliegue: {e}")
            return False

    def _create_install_script(self) -> str:
        """Crea script de instalación para el paquete"""
        if platform.system() == "Windows":
            return f'''@echo off
echo "🚀 Instalando CORA-Quantum Assistant..."
echo.

REM Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python -m venv "{self.venv_name}"

REM Activar entorno virtual
echo "🔧 Activando entorno virtual..."
call "{self.venv_name}/Scripts/activate.bat"

REM Instalar dependencias
echo "📦 Instalando dependencias..."
"{self.venv_name}/Scripts/pip.exe" install -r requirements.txt

REM Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import core.cora_quantum_assistant; print('✅ Instalación exitosa')"

echo.
echo "🎉 Instalación completada!"
echo "Para iniciar: python main.py"
pause
'''
        else:
            return f'''#!/bin/bash
echo "🚀 Instalando CORA-Quantum Assistant..."
echo

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv "{self.venv_name}"

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source "{self.venv_name}/bin/activate"

# Instalar dependencias
echo "📦 Instalando dependencias..."
"{self.venv_name}/bin/pip" install -r requirements.txt

# Verificar instalación
echo "🔍 Verificando instalación..."
python3 -c "import core.cora_quantum_assistant; print('✅ Instalación exitosa')"

echo
echo "🎉 Instalación completada!"
echo "Para iniciar: python3 main.py"
'''

    def run_deployment(self, create_package: bool = False) -> bool:
        """Ejecuta despliegue completo"""
        print("🚀 DESPLIEGUE AUTOMATIZADO - CORA-Quantum Assistant")
        print("=" * 60)
        print("Fecha: 1 de octubre de 2025")
        print("Versión: 1.0 - Prototipo Inicial")
        print()

        # Paso 1: Verificar requisitos del sistema
        requirements = self.check_system_requirements()
        if not all(requirements.get('python_ok', True) for req in [requirements] if 'ok' in req):
            print("❌ Requisitos del sistema no cumplidos")
            return False

        # Paso 2: Crear entorno virtual
        if not self.create_virtual_environment():
            return False

        # Paso 3: Instalar dependencias
        if not self.install_dependencies():
            return False

        # Paso 4: Ejecutar pruebas básicas
        if not self.run_basic_tests():
            print("⚠️  Algunas pruebas fallaron, pero el despliegue continúa...")

        # Paso 5: Crear scripts de inicio
        if not self.create_startup_scripts():
            return False

        # Paso 6: Crear paquete de despliegue (opcional)
        if create_package:
            if not self.create_deployment_package():
                print("⚠️  Error creando paquete de despliegue")

        print("\n🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE!")
        print("=" * 60)
        print("Para usar el sistema:")
        print(f"1. Activar entorno: {self.venv_path / ('Scripts/activate.bat' if platform.system() == 'Windows' else 'bin/activate')}")
        print("2. Ejecutar aplicación: python main.py")
        print("3. O usar script de inicio creado automáticamente")

        return True

def main():
    """Función principal de despliegue"""
    import argparse

    parser = argparse.ArgumentParser(description='Despliegue automatizado de CORA-Quantum Assistant')
    parser.add_argument('--package', action='store_true',
                       help='Crear paquete de despliegue adicional')
    parser.add_argument('--venv', type=str, default=None,
                       help='Nombre del entorno virtual personalizado')

    args = parser.parse_args()

    # Crear gestor de despliegue
    deployer = DeploymentManager()

    if args.venv:
        deployer.venv_name = args.venv
        deployer.venv_path = deployer.project_root / args.venv

    # Ejecutar despliegue
    success = deployer.run_deployment(create_package=args.package)

    if success:
        print("\n✅ Despliegue completado exitosamente!")
        print("\nPróximos pasos:")
        print("1. Revisar la documentación en README.md")
        print("2. Ejecutar ejemplos en la carpeta examples/")
        print("3. Personalizar configuración en config.py")
        print("4. Ejecutar pruebas con test_comprehensive.py")
    else:
        print("\n❌ Despliegue falló")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())