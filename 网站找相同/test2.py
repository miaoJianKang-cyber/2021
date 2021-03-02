# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




opt = Options()
opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
driver = webdriver.Chrome(options=opt)  # 创建无界面对象


urls = []
urls.append("https://www.goldenlaser.cc/")
urls.append("https://www.robamworld.com/")
urls.append("https://www.huaihaiglobal.com/")
urls.append("https://global.linyang.com/")
urls.append("https://www.linttop.com/")
urls.append("https://www.apolomed.com/")
urls.append("https://www.ccic-fct.com/")
urls.append("https://en.xizielevator.com/")
urls.append("https://www.luxotent.com/")

# driver.get(urls)
jj=1
for i in urls:
    driver.get(i)
    driver.maximize_window()
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    fileName = "test"+str(jj)+".html"
    print(fileName)
    f = open(fileName, 'w')
    f.write(str(soup.prettify().encode('utf-8')))
    f.close()
    jj = jj+1
