import pyautogui
import time
# Esse script fica movendo o mouse pra várias direções pra a ligação não cair no discord hehehehe
def avoid_afk(interval=60):
    try:
        print("Press Ctrl+C to stop.")
        while True:
            pyautogui.moveRel(1, 0, duration=0.5)
            pyautogui.moveRel(-1, 0, duration=0.5)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nParado pelo usuário.")

if __name__ == "__main__":
    avoid_afk()
