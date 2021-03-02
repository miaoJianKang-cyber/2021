import time
import pymouse
import pykeyboard
m = pymouse.PyMouse()   # 获取鼠标指针对象
# k = pykeyboard.PyKeyboard()
for i in range(1,20):
    print(m.position())    # 获取当前鼠标指针的坐标
    time.sleep(0.5)



# x = 100
# y = 100
# m.move(x, y)   # 鼠标移动(x,y)坐标
# m.click(3,5)   # 在(x,y)坐标左击
# m.click(x, y, 2)   # 右击

'''
import pyautogui
pyautogui.moveTo(100,100)
pyautogui.click(100,100)

'''
