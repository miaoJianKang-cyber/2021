import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
wait = WebDriverWait(brower, 5)

def getTaobaoCookies():
    # get login taobao cookies
    url = "https://oa.globalso.com/"
    brower.get("https://oa.globalso.com/login")
    while True:
        print("Please login")
        time.sleep(3)
        # if login in successfully, url  jump to www.taobao.com
        while brower.current_url ==  url:
            tbCookies  = brower.get_cookies()
            brower.quit()
            cookies = {}
            for item in tbCookies:
                cookies[item['name']] = item['value']
            outputPath = open('waiMaoBang.pickle','wb')
            pickle.dump(cookies,outputPath)
            outputPath.close()
            return cookies

def readTaobaoCookies():
    # if hava cookies file ,use it
    # if not , getTaobaoCookies()
    if os.path.exists('waiMaoBang.pickle'):
        readPath = open('waiMaoBang.pickle','rb')
        tbCookies = pickle.load(readPath)
    else:
        tbCookies = getTaobaoCookies()
    return tbCookies



tbCookies = readTaobaoCookies()

brower.get("https://oa.globalso.com/")
for cookie in tbCookies:
    brower.add_cookie({
        "domain":"oa.globalso.com",  # 这里需要改
        "name":cookie,
        "value":tbCookies[cookie],
        "path":'/',
        "expires":None
    })
brower.get("https://oa.globalso.com/")
time.sleep(50)