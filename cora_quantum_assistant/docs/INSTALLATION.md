# Guía de Instalación - CORA-Quantum Assistant

## Instalación Rápida

### 1. Descargar el Proyecto
```bash
# El proyecto ya está disponible en el directorio cora_quantum_assistant/
cd cora_quantum_assistant
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar Instalación
```python
from cora_quantum_assistant.core.cora_quantum_assistant import CORAQuantumAssistant
assistant = CORAQuantumAssistant()
print("Instalación exitosa")
```

## Uso Básico

### Ejecutar Asistente Cuántico
```python
from cora_quantum_assistant.core.cora_quantum_assistant import CORAQuantumAssistant

# Inicializar
assistant = CORAQuantumAssistant()

# Ejecutar tarea de optimización
result = assistant.execute_quantum_task('optimization',
    problem_data={'size': 50, 'complexity': 'high'
})

print(f"Éxito: {result['success']}")
```

### Ejecutar Simulador Híbrido
```python
from cora_quantum_assistant.hybrid_simulator.hybrid_quantum_simulator import HybridQuantumSimulator

# Inicializar simulador
simulator = HybridQuantumSimulator()

# Definir función de costo
def cost_function(x):
    return sum(x**2)

# Ejecutar simulación
result = simulator.simulate(cost_function,
[
    1,
    2,
    3
])
print(f"Modo usado: {result.mode_used}")
```

## Archivos Incluidos

- `core/cora_quantum_assistant.py` - Asistente cuántico principal
- `hybrid_simulator/hybrid_quantum_simulator.py` - Simulador híbrido
- `quantum_omega_language/*.qo` - Ejemplos en Quantum-Ω
- `requirements.txt` - Dependencias necesarias
- `README.md` - Documentación completa

## Ejemplos de Código Quantum-Ω

Ver archivos en `quantum_omega_language/` para ejemplos completos de:
- Optimización básica con QOA
- Machine Learning cuántico con QML
- Algoritmos avanzados de optimización

## Solución de Problemas

1. Si falta Qiskit: `pip install qiskit qiskit-aer`
2. Si hay errores de memoria: reducir configuración de qubits
3. Si hay problemas de coherencia: verificar estado del sistema

## Próximos Pasos

1. Revisar ejemplos en archivos `.qo`
2. Ejecutar demostraciones incluidas
3. Personalizar configuración según necesidades
4. Integrar con sistemas CORA existentes

---
*Fecha: 1 de octubre de 2025 - Versión 1.0*