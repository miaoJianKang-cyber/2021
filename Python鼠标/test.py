import pyautogui
import time
# 获取当前屏幕分辨率

time.sleep(5)
screenWidth, screenHeight = pyautogui.size()
pyautogui.press('enter')
for i in range(1,10):
    pyautogui.scroll(-1000)  #鼠标滚轮向下
    time.sleep(1)
for i in range(1,100):
# 获取当前鼠标位置
    currentMouseX, currentMouseY = pyautogui.position()
    print(currentMouseX,currentMouseY)
    time.sleep(0.5)