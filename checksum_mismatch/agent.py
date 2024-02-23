   
import pyautogui

class Agent:
    def __init__(self) -> None:
        print(pyautogui.size())
        currentMouseX, currentMouseY = pyautogui.position()
        print(currentMouseX, currentMouseY)
        pyautogui.moveTo(2995, 89)