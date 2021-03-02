# -*- coding: UTF-8 -*-


from selenium import webdriver


# 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

url = "https://www.baidu.com/"
driver.get(url)