# Inicio Rápido - CORA-Quantum Assistant

## Instalación Automatizada (Recomendada)

### Método 1: Script de Despliegue Automático

```bash
# 1. Ejecutar despliegue automatizado
python deploy.py

# 2. (Opcional) Crear paquete de despliegue
python deploy.py --package
```

### Método 2: Instalación Manual Paso a Paso

```bash
# 1. Crear entorno virtual
python -m venv cora_quantum_env

# 2. Activar entorno virtual
# Windows:
cora_quantum_env\Scripts\activate.bat
# Linux/Mac:
source cora_quantum_env/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python -c "import core.cora_quantum_assistant; print('✅ Instalación exitosa')"
```

## Inicio Rápido

### 1. Modo Interactivo (Recomendado para exploración)

```bash
python main.py --mode interactive
```

### 2. Demostración Automática

```bash
python main.py --mode demo
```

### 3. Configuración Inicial

```bash
python config.py
```

## Ejemplos de Uso

### Ejemplo Básico de Optimización

```python
from core.cora_quantum_assistant import CORAQuantumAssistant

# Inicializar asistente
assistant = CORAQuantumAssistant()

# Ejecutar optimización cuántica
result = assistant.execute_quantum_task('optimization',
{
    'size': 50,
    'complexity': 'high'
})

print(f"Ventaja cuántica: {result['optimization_result'].quantum_advantage*100:.1f}%")
```

### Ejemplo con Simulador Híbrido

```python
from hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator

# Inicializar simulador
simulator = HybridQuantumSimulator()

# Definir función de costo
def cost_function(x):
    return sum(x**2)

# Ejecutar simulación automática
result = simulator.simulate(cost_function,
[
    1,
    2,
    3,
    4,
    5
])
print(f"Modo usado: {result.mode_used}")
print(f"Solución: {result.solution}")
```

### Ejemplo con Lenguaje Quantum-Ω

```python
# Código Quantum-Ω
omega_code = """
quantum_program "optimizacion_basica" {
    version: "1.0"
    qubits: 50

    quantum_function optimizar() -> vector[
        10
    ] {
        qregister qreg[
            10
        ]

        for i in 0..9 {
            H(qreg[i
            ])
        }

        QOA {
            register: qreg
            cost_func: costo_cuadratico
            iterations: 1000
        }

        return optimal_vector
    }
}
"""

# Ejecutar código
result = assistant.execute_quantum_task('omega_code', code=omega_code)
```

## Comandos Útiles

### Configuración del Sistema

```bash
# Configuración automática del entorno
python config.py

# Verificación de integración de componentes
python verify_integration.py

# Ejecutar pruebas básicas
python test_cora_basic.py

# Ejecutar pruebas completas
python test_comprehensive.py
```

### Ejemplos Prácticos

```bash
# Ejecutar ejemplos de aplicaciones reales
python examples/practical_examples.py

# Ejemplo específico de optimización de portafolio
python -c "
from examples.practical_examples import PracticalExamples
examples = PracticalExamples()
examples.example_portfolio_optimization()
"
```

## Solución de Problemas

### Problema: Error de importación de Qiskit

```bash
# Instalar manualmente Qiskit
pip install qiskit qiskit-aer

# Verificar instalación
python -c "import qiskit; print('Qiskit OK')"
```

### Problema: Memoria insuficiente

```python
# Reducir configuración en config.py
config = QuantumConfig(qubits=100, classical_bits=10)

# O usar simulador híbrido con límites
sim_config = SimulationConfig(max_qubits=200, classical_memory_limit=2*1024*1024*1024)
```

### Problema: Coherencia cuántica perdida

```python
# Verificar estado del sistema
status = assistant.get_system_status()
if not status['coherence_status'
]:
    print("Coherencia perdida - reiniciar sistema")
```

## Recursos Adicionales

- 📖 **Documentación completa**: `README.md`
- 🔧 **Guía de instalación detallada**: `docs/INSTALLATION.md`
- 💡 **Especificaciones técnicas**: `ESPECIFICACIONES_ASISTENTE_LENGUAJE_CUANTICO.md`
- 🧪 **Pruebas y ejemplos**: `test_comprehensive.py`, `examples/`
- 📚 **Ejemplos Quantum-Ω**: `quantum_omega_language/examples.qo`

## Próximos Pasos

1. **Explorar ejemplos prácticos** en la carpeta `examples/`
2. **Personalizar configuración** según tus necesidades en `config.py`
3. **Revisar documentación técnica** para características avanzadas
4. **Ejecutar pruebas completas** para verificar funcionamiento
5. **Integrar con aplicaciones existentes** usando la API del asistente

## Soporte

Para problemas o preguntas:

1. Revisar los logs de ejecución
2. Ejecutar `python verify_integration.py` para diagnóstico
3. Consultar la documentación en `README.md`
4. Ejecutar pruebas con `python test_comprehensive.py`

---

**¡Bienvenido al futuro de la computación cuántica con CORA-Quantum Assistant!** ⚛️

*Documento generado automáticamente - 1 de octubre de 2025*