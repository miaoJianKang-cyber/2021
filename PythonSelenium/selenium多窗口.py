import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 成功
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

browersDriver = webdriver.Chrome()
# browersDriver.get()
for i in range(0, 10):
    browersDriver.execute_script('window.open("https://www.baidu.com/")')

window_list = browersDriver.window_handles  # 获取窗口列表
# browersDriver.switch_to.window(window_list[0])  # 将browers_driver的指针转移到指定的窗口
# print(browersDriver.current_url)  # 打印browers_driver指向的窗口网址


# is_disappeared = WebDriverWait(browersDriver, 8, 0.5, ignored_exceptions=TimeoutException).until(lambda x: x.find_element_by_id("kw").is_displayed())

# print(WebDriverWait(browersDriver, 0).until(EC.title_is(u"百度一下，你就知道")))
# print(WebDriverWait(browersDriver, 0).until(EC.title_contains(u"知道")))
# print(WebDriverWait(browersDriver, 0).until(EC.visibility_of_element_located((By.ID, 'su'))))

# print(is_disappeared)
window_list.reverse()
for i in window_list:

    browersDriver.switch_to.window(i)
    if browersDriver.current_url == "data:,":
        print("aa")
        continue
    else:
        print(browersDriver.current_url)
        browersDriver.close()
        time.sleep(1)