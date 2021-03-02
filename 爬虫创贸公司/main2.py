import csv
import io
import sys
import time  # 引入time模块
from selenium import webdriver
from bs4 import BeautifulSoup
import pymouse


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def beforeWork():
    driver = webdriver.Chrome()
    driver.get('https://oa.globalso.com/admins')
    driver.maximize_window()
    return driver
    pass


def login(driver):
    driver.find_element_by_id('user_login').send_keys("18003962410")
    # driver.find_element_by_id('btn_yzm').click()
    while True:
        print("Please login")
        time.sleep(3)
        while driver.current_url == 'https://oa.globalso.com/':
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="sys-info-pop"]/div/span').click()
            return True


def getGongHai(driver):
    # !!!!!!!!!!平台（7W+）
    driver.get('https://oa.globalso.com/high_seas/platform')
    m = pymouse.PyMouse()
    jj=0
    for i in range(1, 473):
        if i>100:
            jj=20
        main_handle = driver.current_window_handle
        time.sleep(1)
        for k in range(1, 14):
            m.click(1900, 964)
        for kk in range(1, 30):
            m.click(1900, 975)
        # 开始
        inframe = driver.find_element_by_class_name('iframe-box')
        driver.switch_to.frame(inframe)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        trs = soup.find_all('tr', {'class': 'data-item'})
        tds = soup.find_all('td', {'colspan': '11'})  # ---------------------------------------------------------------->平台

        data_list = []
        for j in range(len(trs)):
            try:
                for line in trs[j].children:
                    try:
                        data_list.append(line.string)
                    except:
                        print('第{}页，第{}个数据格式错误'.format(i, j))
                for line in tds[j].children:
                    try:
                        data_list.append(line.string)
                    except:
                        print('第{}页，第{}个数据格式错误'.format(i, j))
                try:
                    with open('2allData2.csv', 'a', newline="") as filecsv:
                        caswriter = csv.writer(filecsv)
                        caswriter.writerow(data_list)
                except:
                    print("{}{}".format(i,j))
                data_list = []
            except:
                print(i,'i')
        driver.switch_to.window(main_handle)
        driver.maximize_window()
        m.click(int(1142 + int(int(i) * 0.1)+int(jj)), 891)
        time.sleep(1)

        # 结束

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
