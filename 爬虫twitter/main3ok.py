# url爬取
# 保存到csv文件

import csv
import io
import sys
import time  # 引入time模块
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def openChrome():
    # get直接返回，不再等待界面加载完成
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"

    # 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)

    # 设置无界面模式
    opt = Options()
    opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
    opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
    opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
    opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
    driver = webdriver.Chrome(options=opt)  # 创建无界面对象


    url = "https://twitter.com/search?q="+keyword+"&src=typed_query"
    driver.get(url)
    return driver


def getData(driver):
    time.sleep(3)
    for i in range(1, 10):
        time.sleep(1)
        driver.maximize_window()
        js = 'window.scrollBy(0,1000)'
        driver.execute_script(js)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
        for div in divs:
            data_list = []
            try:
                name = div.find(
                    'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
                data_list.append(name)
                user_name = div.find(
                    'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd'}).get_text()
                data_list.append(user_name)
                date = soup.find('a',
                                 class_='css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')
                date = str(date)
                dateSta = str(date).find('datetime') + 10
                dateSto = str(date).find('">', dateSta)
                date = date[dateSta:dateSto]
                data_list.append(date)
                content = div.find('div', {
                    'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}).descendants
                contentData = ''
                flagi = True
                for j in content:
                    if flagi:
                        flagi = False
                        contentData += str(j.string)
                    else:
                        flagi = True
                data_list.append(contentData.strip().replace('\n', ''))
            except :
                print("获取数据错误一次")
            try:
                with open('allData1.csv', 'a',newline="",encoding='utf-8') as filecsv:  # ------------------------------------------->保存的文件名
                    caswriter = csv.writer(filecsv)
                    caswriter.writerow(data_list)
            except :
                print("保存数据错误一次")
    pass
def allProcess():
    # 打开浏览器
    driver = openChrome()
    # 开始爬取
    getData(driver)

if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    keyword = "mask"
    allProcess()
    print("Stop at:", time.asctime(time.localtime(time.time())))
