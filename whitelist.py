import pyautogui
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

time.sleep(5)
def connect(server):
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab')
    for i in range(0, 20):
        pyautogui.press('backspace')
    pyautogui.write(server)
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(6)
    img = pyautogui.screenshot()
    text = pytesseract.image_to_string(img)
    if "whitelist" in text:
        pyautogui.press('tab')
        pyautogui.press('enter')
        return True
    else:
        pyautogui.press('esc')
        for i in range(7):
            pyautogui.press('tab')
        pyautogui.press('enter')
        return False


print(connect('baum-server.de'))
print(connect('93.186.198.89:25565'))


