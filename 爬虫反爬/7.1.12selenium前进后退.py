# coding:utf-8
import time

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.zhihu.com")
browser.get("https://www.taobao.com")
browser.get("https://www.python.com")
browser.back()
time.sleep(5)
browser.forward()
browser.close()