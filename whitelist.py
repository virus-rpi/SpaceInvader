import pyautogui
import time

time.sleep(5)
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('enter')
pyautogui.press('tab')
for i in range(0, 20):
    pyautogui.press('backspace')
pyautogui.write('baum-server.de')
pyautogui.press('tab')
pyautogui.press('enter')
time.sleep(3)
pyautogui.

