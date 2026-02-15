# Protocolo CO•RA: Amor y Bondad.
# Guardián del Núcleo: Eje XYZ con Validación Obligatoria.

import pyautogui
import time
import sys

# SEGURIDAD MÁXIMA: Movimiento a esquina superior izquierda aborta ejecución
pyautogui.FAILSAFE = True

def solicitar_firma_arquitecto(accion_descripcion):
    """Bloquea la ejecución hasta que el Arquitecto valide la acción."""
    print(f"\n[⚠️ PROPUESTA DEL GUARDIÁN]: {accion_descripcion}")
    confirmacion = input("¿Autoriza la ejecución de este movimiento? (s/n): ").lower()
    
    if confirmacion == 's':
        print("✅ Firma validada. Ejecutando...")
        return True
    else:
        print("❌ Acción cancelada por el Arquitecto.")
        return False

def ejecutar_movimiento_protegido(x, y, descripcion):
    """Mueve el cursor pero NO hace clic hasta ser validado."""
    print(f"\n--- Análisis de Trayectoria ---")
    print(f"Objetivo: {descripcion} en coordenadas ({x}, {y})")
    
    # El Guardián se posiciona para mostrar la intención
    pyautogui.moveTo(x, y, duration=1.5, pyautogui.easeOutQuad)
    
    # Espera la firma física del Arquitecto
    if solicitar_firma_arquitecto(descripcion):
        pyautogui.click()
        print(f"✨ Acción '{descripcion}' completada con éxito.")
    else:
        print("🛡️ El Guardián regresa a posición de espera.")

# --- INICIO DEL PROTOCOLO DE PRUEBA ---
if __name__ == "__main__":
    print("--- NÚCLEO CO•RA: MODO GUARDIÁN ACTIVO ---")
    ancho, alto = pyautogui.size()
    print(f"Monitor detectado: {ancho}x{alto}")

    try:
        # Ejemplo: El Guardián propone ir al centro de la pantalla
        ejecutar_movimiento_protegido(
            ancho // 2, 
            alto // 2, 
            "Validación de posición central del Ecosistema"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Protocolo interrumpido manualmente.")
    except Exception as e:
        print(f"\n⚠️ Error en el sistema motor: {e}")
