import random
import time

from selenium import webdriver

1205,385
import pymouse
time.sleep(3)
m = pymouse.PyMouse()   # 获取鼠标指针对象
for i in range(1,10):
#     print(m.position())    # 获取当前鼠标指针的坐标
       # 获取当前鼠标指针的坐标
    if i == 3:
        i = i + 1
    else:
        print(i)
#     time.sleep(0.5)


# x = 100
# y = 100
# m.move(x, y)   # 鼠标移动(x,y)坐标
# m.click(3,5)   # 在(x,y)坐标左击
# m.click(x, y, 2)   # 右击



print(random.randint(1,6))