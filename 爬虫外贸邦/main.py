import collections
import csv
import io
import json
import sys
import time  # 引入time模块
from selenium import webdriver


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def beforeWork():
    driver = webdriver.Chrome()
    driver.get('https://www.52wmb.com/')
    driver.maximize_window()
    return driver
    pass

def login(driver):
    driver.find_element_by_xpath('//*[@id="_body"]/div[2]/nav/div/div/div[2]/div[1]/a[1]').click()
    time.sleep(1.5)
    driver.find_element_by_name('signusername').clear()
    driver.find_element_by_name('signusername').send_keys('18637371787')
    driver.find_element_by_name('signpassword').clear()
    driver.find_element_by_name('signpassword').send_keys('hpd12345678')
    driver.find_element_by_name('loginsubmit').click()

    try:
        driver.get('https://www.52wmb.com/buyer')
    except:
        return False
    else:
        return True

def getHsCode():
    with open('comanyName.txt') as f:
        comanyNameAll = f.readlines()
    for comanyNameNow in comanyNameAll:
        file = open('data\\kp.csv', 'a+', encoding='utf-8', newline="")
        file_write = csv.writer(file)
        file_write.writerow(['day', 'company_name', 'number', 'country', 'email', 'lianxiren', 'phone', 'address', 'website','update_time', 'tableid', 'is_spider'])
    with open('adjunct.json') as f:
        con_dict = json.loads(f.read())
    mysqlDb = con_dict[comanyNameNow]['datebase']
    dataHs = con_dict[comanyNameNow]['hs']
    try:
        dataHs = dataHs.split(',')
    except Exception as e:
        print('无需分割' + e)
    print('当前此hs无需分割',dataHs)
    return dataHs
    pass

def getHsProduct(dataHs,driver):

    driver.find_element_by_xpath('//*[@id="search-type-select"]/i').click()
    time.sleep(1.6)
    driver.find_element_by_xpath('//*[@id="search-select-ul"]/li[4]').click()
    # driver.find_element_by_id('search-select-ul').click()

    # action = ActionChains(driver)
    # action.move_to_element_with_offset(0, 100).click()
    # action.move_by_offset(600, 300).click()

    # driver.find_element_by_xpath('//ul[@ul="select-ul"]/li[4]').click()
    # driver.find_element_by_xpath('//*[@id="search-select-ul"]/li[4]').click()
    time.sleep(1)

    print(dataHs)
    # for hs in dataHs:
    #     driver.find_element_by_class_name('seach-text input-company-search').send_keys(hs)
    #     driver.find_element_by_xpath('//*[@id="clickSearchbtn"]').click()
    #
    #     pass


    # for hs in dataHs:
    #     dataHsOne = collections.OrderedDict()
    #     dataHsOne['key'] = hs
    #     print('dataHsOne',dataHsOne)
    #
    #     pass
    pass


def main():
    # 准备工作
    driver = beforeWork()
    # 登录
    time.sleep(5)
    result = login(driver)
    if result:
        print("登录成功")
        # 获取hs编码
        time.sleep(5)
        dataHs=getHsCode()
        # 获取该Hs下的产品
        getHsProduct(dataHs,driver)

    else:
        print("登录失败！")
        print("请手动验证登录信息")
    time.sleep(10)


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    main()
    print("Stop at:", time.asctime(time.localtime(time.time())))
