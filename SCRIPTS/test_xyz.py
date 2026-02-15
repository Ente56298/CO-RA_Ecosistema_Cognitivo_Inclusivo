"""// Protocolo CO•RA: Amor y Bondad.

Prueba básica de PyAutoGUI para el ecosistema CO•RA.
Este script activa el FAILSAFE para permitir abortar moviendo el cursor a la esquina superior izquierda.
"""

import pyautogui
import time

pyautogui.FAILSAFE = True

def main():
    print("Protocolo CO•RA activo: Amor y Bondad.")
    try:
        size = pyautogui.size()
        print(f"Screen size: {size}")
        time.sleep(1)
        # Movimiento suave a coordenadas (100,100)
        pyautogui.moveTo(100, 100, duration=0.5)
        print("Movimiento completado. Mueve el cursor a la esquina superior izquierda para abortar si es necesario.")
    except Exception as e:
        print("Error al ejecutar PyAutoGUI:", e)


if __name__ == '__main__':
    main()