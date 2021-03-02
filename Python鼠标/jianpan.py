import pyautogui


#模拟输入信息
pyautogui.typewrite(message='Hello world!',interval=0.5)
#点击ESC
pyautogui.press('esc')
pyautogui.press('enter')
# 按住shift键
pyautogui.keyDown('shift')
# 放开shift键
pyautogui.keyUp('shift')
# 模拟组合热键
pyautogui.hotkey('ctrl', 'c')