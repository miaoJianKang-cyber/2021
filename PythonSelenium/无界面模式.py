# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 设置无界面模式
opt = Options()
opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
driver = webdriver.Chrome(options=opt)  # 创建无界面对象

url = "https://www.baidu.com/"
driver.get(url)

# 崔庆才: 无界面模式
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)