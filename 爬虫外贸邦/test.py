"""
作者：苗建康
开始时间：2021年1月7日17:27:31
结束时间：
功能：爬取Twitter上发布购买需求的购买者的主页、内容、手机号或者邮箱
爬取入口：https://twitter.com/home
"""

import io
import sys
import time  # 引入time模块
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def beforeWork():
    driver = webdriver.Chrome()
    driver.get('https://twitter.com/home')
    driver.maximize_window()
    return driver
    pass


def login(driver):
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input').send_keys("miao80254112")
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input').send_keys('MIao2493')
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div').click()
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[2]/div/div/div[2]/div/div[2]/div')
    except:
        return False

    else:
        return True


def search_content(driver, keyword):
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(keyword)
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input').send_keys(Keys.ENTER)
    try:
        driver.find_element_by_class_name('css-1dbjc4n')
    except:
        return False
    else:
        return True
    pass


# 已经查找成功，获取内容
def get_content(driver):
    # 获取内容
    time.sleep(5)
    Data_List = []
    for i in range(500):
        js = 'window.scrollBy(0,1000)'
        driver.execute_script(js)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
        print('Fetching data on page {}！！！'.format(i))
        for div in divs:
            data_list = []
            name = div.find(
                'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
            data_list.append(name)
            user_name = div.find(
                'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd'}).get_text()
            data_list.append(user_name)
            date = div.find('a', {
                'class': 'css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0'})
            date = soup.find('a',class_='css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')
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
        time.sleep(3)
        if(i%100==0 and i!=0):
            save(Data_List,str(i))
            Data_List = []
    pass


def save(Data_List_New,sheetData):
    try:
        print('共爬取了 {} 条数据。'.format(len(Data_List_New)))
        df_Sheet = pandas.DataFrame(Data_List_New, columns=['name', 'user_name', 'date', 'content'])

        writer = pandas.ExcelWriter('twitterXlsx09'+str(sheetData)+'.xlsx')
        df_Sheet.to_excel(excel_writer=writer, sheet_name='twitter', index=None)
        writer.save()
        writer.close()
    except:
        print("数据格式错误")
        print(Data_List_New)


def main(keyword):
    # 准备工作
    driver = beforeWork()
    # 登录
    time.sleep(5)
    result = login(driver)
    if result:
        print("登录成功")
        # 查找
        time.sleep(5)
        searchResult = search_content(driver, keyword)
        if searchResult:
            print("搜索成功")
            # 获取内容
            driver.implicitly_wait(10)  # 浏览器等待
            get_content(driver)
            # 保存数据

            # 结束
            print("结束")
        else:
            print('搜索失败，请处理')
    else:
        print("登录失败！")
        print("请手动验证登录信息")
    time.sleep(10)

if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    keyword = "mask "
    main(keyword)
    print("Stop at:", time.asctime(time.localtime(time.time())))
