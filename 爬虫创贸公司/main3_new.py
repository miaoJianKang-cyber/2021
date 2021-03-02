import csv
import io
import random
import sys
import time  # 引入time模块
from selenium import webdriver
from bs4 import BeautifulSoup



sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def beforeWork():
    driver = webdriver.Chrome()
    driver.get('https://oa.globalso.com/admins')
    driver.maximize_window()
    return driver
    pass


def login(driver):
    driver.find_element_by_id('user_login').send_keys("18003962410")
    driver.find_element_by_id('btn_yzm').click()
    while True:
        while driver.current_url == 'https://oa.globalso.com/':
            time.sleep(1)
            return True


def getGongHai(driver):
    # !!!!!!!!!!平台（7W+）
    driver.get('https://oa.globalso.com/high_seas/independent') # ------------------------------------------------------>域名地址[已改]
    inframe = driver.find_element_by_class_name('iframe-box')
    driver.switch_to.frame(inframe)
    time.sleep(2)
    for i in range(1, 4611): # ----------------------------------------------------------------------------------------->页数[已改]
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr', {'class': 'data-item'})
        tds = soup.find_all('td', {'colspan': '9'})  # ---------------------------------------------------------------->独立站[]
        data_list = []
        for j in range(len(trs)):
            try:
                for line in trs[j].children:
                    try:   # 获取数据
                        data_list.append(line.string)
                    except:
                        print('第{}页，第{}个数据格式错误'.format(i, j))
                for line in tds[j].children:
                    try:  # 获取数据
                        data_list.append(line.string)
                    except:
                        print('第{}页，第{}个数据格式错误'.format(i, j))
                try:   # 保存数据
                    with open('3allData20210123_3.csv', 'a', newline="") as filecsv: # ------------------------------------------->保存的文件名
                        caswriter = csv.writer(filecsv)
                        caswriter.writerow(data_list)
                except:
                    pass
                data_list = []
            except:
                pass
        flag_page = True
        while flag_page:
            try:
                if i == 1:
                    driver.find_element_by_xpath('//*[@id="page"]/a[6]').click()  # 下一页
                elif i == 2 or i == 3:
                    driver.find_element_by_xpath('//*[@id="page"]/a[8]').click()  # 下一页
                elif i == 4 or i == 72:  # 特殊页：点下一页网站方面出错
                    driver.find_element_by_xpath('//*[@id="page"]/a[7]').click()
                    i = i + 1
                elif i >= 6:
                    driver.find_element_by_xpath('//*[@id="page"]/a[8]').click()  # 下一页
                flag_page = False
            except:
                time.sleep(3)
                driver.refresh()
        time.sleep(random.randint(1,2))
        # 结束
        print("第{}页出错".format(i))




def main():
    # 准备工作
    driver = beforeWork()
    result = login(driver)
    if result:
        print("登录成功")

        # 到公海页面，返回总页数，
        time.sleep(2)
        getGongHai(driver)



    else:
        print("登录失败,请手动验证登录信息")
    time.sleep(100)
    pass


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    main()
    print("Stop at:", time.asctime(time.localtime(time.time())))
