   
import pyautogui
import pyperclip
import time


class BaseAgent:
    def __init__(self) -> None:
        print(pyautogui.size())
        currentMouseX, currentMouseY = pyautogui.position()
        print("BaseAgent initialized")
        
    def loadWebPage(self, address):
        pyautogui.click(201, 66)
        pyautogui.press('backspace')
        pyautogui.write(address)
        pyautogui.press('enter')
        time.sleep(1)
    
    def webPageActions(self):
        pass

    def execute(self, address):
        self.loadWebPage(address)
        self.webPageActions()
        data = pyperclip.paste()
        return data

class RucioWebUIAgent(BaseAgent):
    """Extracts adler32 checksum from Rucio Web UI
    """
    def __init__(self) -> None:
       super().__init__()

    def webPageActions(self):
        pyautogui.rightClick(764, 315)
        pyautogui.click(787, 355)
        time.sleep(1)
        checksum = pyperclip.paste()
        return checksum

class FTSLogScrapingAgent:
    """Scrapes FTS logs for transfer details
    """
    def __init__(self) -> None:
        pass

    def execute(self, address):
        pass
