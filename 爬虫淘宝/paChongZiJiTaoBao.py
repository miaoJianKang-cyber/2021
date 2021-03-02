"""
作者：苗建康
编成时间：2021年1月7日04:15:55
输入：https://i-suo.en.alibaba.com/productlist.html?spm=a2700.shop_index.88.17
输出：该阿里巴巴店家全部商品的名称和价格
"""

import io
import sys
import time  # 引入time模块
from selenium import webdriver
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
# # 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
#
#
# driver = webdriver.Chrome(chrome_options=chrome_options)

def get_product():
    driver.maximize_window()
    # time.sleep(10)
    divss = driver.find_elements_by_xpath(
        '//div[@class="component-product-list"]/div/div[@class="next-row next-row-no-padding next-row-no-wrap gallery-view"]')
    for divs in divss:
        divs_data = divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item"]')
        if divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item last"]')[0].is_displayed():
            divs_data.append(divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item last"]')[0])
        else:
            pass
        for div in divs_data:
            info = div.find_element_by_xpath('.//div[@class="product-info"]/div[@class="title clamped"]/a').text  # 商品名称
            price = div.find_element_by_xpath('.//div[@class="product-info"]/div[@class="price"]').text # 商品价格
            with open('data.csv', 'a', newline="") as filecsv:
                caswriter = csv.writer(filecsv)
                caswriter.writerow([info,price])
    page_max = driver.find_element_by_xpath('//div[@class="next-pagination-list"]/a[6]').text #最大页数
    return page_max
def main():
    print('正在爬取第1页数据')
    page_current = 2
    page_max = get_product()

    while page_current != page_max:
        print('*' * 100)
        print('正在爬取第{}页数据'.format(page_current))
        print('*' * 100)
        driver.get('https://i-suo.en.alibaba.com/productlist-{}.html'.format(page_current))  # 拼接url地址
        driver.implicitly_wait(2)  # 浏览器等待
        driver.maximize_window()  # 最大化浏览器
        page_max = get_product()
        page_current += 1



    print("Stop at:", time.asctime(time.localtime(time.time())))

if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))

    # 开始
    driver = webdriver.Chrome()
    driver.get('https://i-suo.en.alibaba.com/productlist.html?spm=a2700.shop_index.88.17')
    main()
