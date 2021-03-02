import io
import sys
import time  # 引入time模块
from selenium import webdriver
import csv
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def search_product(keyword):
    """模拟搜索"""
    driver.find_element_by_id('mq').send_keys(keyword)
    driver.find_element_by_xpath('//*[@id="J_PopSearch"]/div[1]/div/form/input[2]').click()

    driver.maximize_window()
    time.sleep(15)

    page = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text  # 找页数
    page = re.findall('(\d+)', page)[0]
    return int(page)


def get_product():
    divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        info = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text  # 商品名称
        price = div.find_element_by_xpath('.//strong').text + '元'  # 商品价格
        deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text  # 付款人数
        name = div.find_element_by_xpath('.//div[@class="shop"]/a').text  # 店铺名称
        print(info, price, deal, name, sep='|')
        with open('dataworld.csv', 'a', newline="") as filecsv:
            caswriter = csv.writer(filecsv, delimiter=",")
            caswriter.writerow([info, price, deal, name])
    pass


def main():
    keyword = "trousers"
    print("正在爬取第一页数据")
    page = search_product(keyword)
    print('page=', page)
    get_product()

    page_num = 1
    while page_num != page:
        print('*' * 100)
        print('正在爬取第{}页数据'.format(page_num + 1))
        print('*' * 100)
        driver.get('https://s.taobao.com/search?q={}&s={}'.format(keyword, page_num * 44))  # 拼接url地址
        driver.implicitly_wait(2)  # 浏览器等待
        driver.maximize_window()  # 最大化浏览器
        get_product()
        page_num += 1


if __name__ == '__main__':
    print("Run Ok at->", time.asctime(time.localtime(time.time())))

    # 开始
    # keyword = input("请输入你要搜索的商品关键字： ")

    driver = webdriver.Chrome()
    driver.get('https://world.taobao.com/')
    main()
