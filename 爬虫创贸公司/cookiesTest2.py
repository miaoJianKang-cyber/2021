import os

import requests
import time
import json
from selenium import webdriver


brower = webdriver.Chrome()



def getTaobaoCookies():
    # get login taobao cookies
    url = "https://oa.globalso.com/"
    brower.get("https://oa.globalso.com/login")
    while True:
        print("Please login")
        time.sleep(3)
        # if login in successfully, url  jump to www.taobao.com
        print(brower.current_url)
        while brower.current_url ==  url:
            tbCookies  = brower.get_cookies()
            brower.quit()
            outputPath = open('tbCookies.txt','w')
            outputPath.write(json.dumps(tbCookies))
            outputPath.close()
            return tbCookies

def readTaobaoCookies():
    # if hava cookies file ,use it
    # if not , getTaobaoCookies()
    if os.path.exists('tbCookies.txt'):
        readPath = open('tbCookies.txt')
        cookies = json.loads(readPath.read())
    else:
        cookies = getTaobaoCookies()
    return cookies




cookies = readTaobaoCookies()
driver = webdriver.Chrome()
driver.get("https://oa.globalso.com/")
#使用cookies登录
for cook in cookies:
    driver.add_cookie(cook)
#刷新页面
driver.refresh()
time.sleep(20)
driver.quit()
