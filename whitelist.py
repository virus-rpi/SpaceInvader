import pyautogui
import time
import pytesseract
from dbManeger import dbManeger

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
    if "whitelist" in text or "white-list" in text:
        pyautogui.press('tab')
        pyautogui.press('enter')
        print("True")
        return True
    else:
        pyautogui.press('esc')
        for i in range(7):
            pyautogui.press('tab')
        pyautogui.press('enter')
        print("False")
        return False

def getIps():
    db = dbManeger(r"ip.db")
    ips = db.execute('SELECT ip, port FROM ip WHERE players != "None";')
    return ips

def write(whitelist, nr):
    db = dbManeger(r"ip.db")
    db.execute(f'UPDATE ip SET whitelist = "{str(whitelist)}" WHERE ip = {nr};')



ips = getIps()
db = dbManeger(r"ip.db")
for i in ips:
    ip = i[0]
    port = i[1]
    print(f'{ip}:{port}')
    whitelist = connect(f'{ip}:{port}')
    nr = db.find("ip", f'"{ip}"')[0][0]
    write(whitelist, nr)
