   
import pyautogui
import pyperclip
import time


class BaseAgent:
    def __init__(self) -> None:
        print(pyautogui.size())
        currentMouseX, currentMouseY = pyautogui.position()
        print("BaseAgent initialized")
        print(f"Current mouse position: {currentMouseX}, {currentMouseY}")
        
    def loadWebPage(self, address):
        pyautogui.click(201, 66)
        pyautogui.press('backspace')
        pyautogui.write(address)
        pyautogui.press('enter')
        time.sleep(1)
    
    def webPageActions(self, row):
        pass
    
    def postProcess(self, output):
        pass

    def execute(self, address, row):
        self.loadWebPage(address)
        self.webPageActions(row)
        data = pyperclip.paste()
        data = self.postProcess(data)
        return data

class RucioWebUIAgent(BaseAgent):
    """Extracts adler32 checksum from Rucio Web UI
    """
    def __init__(self) -> None:
       super().__init__()

    def webPageActions(self, row):
        pyautogui.rightClick(764, 315)
        pyautogui.click(787, 355)
        time.sleep(1)
        checksum = pyperclip.paste()
        return checksum

class FTSLogScrapingAgent(BaseAgent):
    """Scrapes FTS logs for transfer details
    """
    def __init__(self) -> None:
        super().__init__()

    def webPageActions(self, row):
        did = row['did']
        pyautogui.click(1311, 855)
        time.sleep(1)
        # x509 certificate
        pyautogui.click(934, 354)
        time.sleep(1)
        # select all
        pyautogui.hotkey('win', 'a')
        # right click
        pyautogui.rightClick(934, 354)
        # save as
        pyautogui.click(979, 471)
        time.sleep(1)
        # save
        pyautogui.write(f"{did}")
        pyautogui.keyDown(key='enter')
        pyautogui.click(775, 578)
    def postProcess(self, output):
        print(output)
