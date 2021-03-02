"""
作者：苗建康
开始时间：2021年1月18日17:27:31
结束时间：
功能：爬取Twitter上发布购买需求的购买者的主页、内容、手机号或者邮箱
爬取入口：https://twitter.com/home
"""

import io
import sys
import time  # 引入time模块
from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import pandas

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def openChrome():
    # get直接返回，不再等待界面加载完成
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"

    # 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://twitter.com/home")
    return driver


def loginID():
    print("由于Twitter反爬技术未实现，请手动登录账号，并在本界面中输入关键字.", end="\n")
    while True:
        keyword = input()
        time.sleep(1)
        if keyword:
            break
        print("请手动登录账号，并在本界面中输入关键字.")
    print("登录账号成功，已获取keyword：{}".format(keyword))
    return keyword


def search(driver, keyword):
    # 向搜索框里输入keyword
    driver.maximize_window()
    pyautogui.moveTo(1290, 140, duration=1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.click()
    pyautogui.typewrite(message=keyword, interval=0.5)
    pyautogui.press('enter')
    pass


def getData(driver):
    for i in range(1, 500):
        pyautogui.scroll(-600)  # 鼠标滚轮向下
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
        Data_List = []
        for div in divs:
            data_list = []
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
            Data_List.append(data_list)
        if (i % 100 == 0 and i != 0):
            saveData(str(i))
            Data_List = []
    pass


def saveData(sheetData):
    try:
        print('现在爬取了 {} 条数据。'.format(len(Data_List)))
        df_Sheet = pandas.DataFrame(Data_List, columns=['name', 'user_name', 'date', 'content'])

        writer = pandas.ExcelWriter('data-Twitter-' + str(sheetData) + '.xlsx')
        df_Sheet.to_excel(excel_writer=writer, sheet_name='twitter', index=None)
        writer.save()
        writer.close()
    except:
        print("数据格式错误")
        print(Data_List)

    pass


def allProcess():
    # 打开浏览器
    driver = openChrome()
    # 登录账号
    keyword = loginID()
    # 搜索keyword
    search(driver, keyword)
    # 开始爬取
    getData(driver)
    # 保存数据
    # saveData() # 在开始爬取方法中已经调用


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    keyword = ""
    Data_List = []
    allProcess()
    print("Stop at:", time.asctime(time.localtime(time.time())))
