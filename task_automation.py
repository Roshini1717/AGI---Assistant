import pyautogui
import time

def automate_task(actions):
    for act in actions:
        if act.get("action") == "click":
            pyautogui.click(act.get("x", 0), act.get("y", 0))
        elif act.get("action") == "type":
            pyautogui.write(act.get("text", ""))
        time.sleep(0.1)
