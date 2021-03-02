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


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"


def get_product():
    driver.maximize_window()
    # 获取当前句柄
    main_handle = driver.current_window_handle
    page_max = driver.find_element_by_xpath('//div[@class="next-pagination-list"]/a[6]').text  # 最大页数
    # 16个：divss
    divss = driver.find_elements_by_xpath('//div[@class="component-product-list"]/div/div[@class="next-row next-row-no-padding next-row-no-wrap gallery-view"]')

    for divs in divss:
        # 4个：divs_data
        divs_data = divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item"]')
        if divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item last"]')[
            0].is_displayed():
            divs_data.append(
                divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item last"]')[0])
        else:
            pass
        # 1个：div
        for div in divs_data:
            div.find_element_by_xpath('.//div[@class="product-info"]/div[@class="title clamped"]/a').click()

            pass

    # 获取所有句柄
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != main_handle:
            driver.switch_to.window(handle)
            all_meta = driver.find_elements_by_css_selector('meta')
            for element_meta in all_meta:
                if (element_meta.get_attribute('name') == 'keywords'):
                    element_data = element_meta.get_attribute('content')
                    print(element_data)
                    if ("Ltd" in element_data):
                        late_data = tuple(element_data.split(','))
                        for i in range(len(late_data) - 2):
                            lata_data_no = (str(late_data[i]))
                            lata_data_no = lata_data_no.replace('High Quality', '')
                            lata_data_no = lata_data_no.replace('OEM', '')
                            lata_data_no = lata_data_no.replace('Best', '')
                            lata_data_no = lata_data_no.replace('Buy', '')
                            lata_data_no = lata_data_no.replace('Discount', '')
                            lata_data_no = lata_data_no.replace('China', '')
                            lata_data_no = lata_data_no.replace('Wholesale', '')
                            lata_data_no = lata_data_no.replace('Products', '')
                            lata_data_no = lata_data_no.replace('Product', '')
                            lata_data_no = lata_data_no.replace('Companies', '')
                            lata_data_no = lata_data_no.replace('Company', '')
                            lata_data_no = lata_data_no.replace('Exporters', '')
                            lata_data_no = lata_data_no.replace('Exporter', '')
                            lata_data_no = lata_data_no.replace('Quotes', '')
                            lata_data_no = lata_data_no.replace('Pricelist', '')
                            lata_data_no = lata_data_no.replace('Factories', '')
                            lata_data_no = lata_data_no.replace('Factory', '')
                            lata_data_no = lata_data_no.replace('Manufacturers', '')
                            lata_data_no = lata_data_no.replace('Suppliers', '')
                            lata_data_no = lata_data_no.replace('Supplier', '')
                            lata_data_no = lata_data_no.replace('Manufacturer', '')
                            lata_data_no = lata_data_no.lstrip()
                            with open('data47.txt', 'a', newline="") as filecsv:
                                caswriter = csv.writer(filecsv)
                                caswriter.writerow([lata_data_no])
                    else:
                        late_data = tuple(element_data.split(','))
                        for i in range(len(late_data)):
                            lata_data_no = (str(late_data[i]))
                            lata_data_no = lata_data_no.replace('High Quality', '')
                            lata_data_no = lata_data_no.replace('OEM', '')
                            lata_data_no = lata_data_no.replace('Best', '')
                            lata_data_no = lata_data_no.replace('Buy', '')
                            lata_data_no = lata_data_no.replace('Discount', '')
                            lata_data_no = lata_data_no.replace('China', '')
                            lata_data_no = lata_data_no.replace('Wholesale', '')
                            lata_data_no = lata_data_no.replace('Products', '')
                            lata_data_no = lata_data_no.replace('Product', '')
                            lata_data_no = lata_data_no.replace('Companies', '')
                            lata_data_no = lata_data_no.replace('Company', '')
                            lata_data_no = lata_data_no.replace('Exporters', '')
                            lata_data_no = lata_data_no.replace('Exporter', '')
                            lata_data_no = lata_data_no.replace('Quotes', '')
                            lata_data_no = lata_data_no.replace('Pricelist', '')
                            lata_data_no = lata_data_no.replace('Factories', '')
                            lata_data_no = lata_data_no.replace('Factory', '')
                            lata_data_no = lata_data_no.replace('Manufacturers', '')
                            lata_data_no = lata_data_no.replace('Suppliers', '')
                            lata_data_no = lata_data_no.replace('Supplier', '')
                            lata_data_no = lata_data_no.replace('Manufacturer', '')
                            lata_data_no = lata_data_no.lstrip()
                            with open('data47.txt', 'a', newline="") as filecsv:
                                caswriter = csv.writer(filecsv)
                                caswriter.writerow([lata_data_no])
            driver.close()

    driver.switch_to.window(main_handle)
    return page_max


def main():
    print('正在爬取第35页数据')
    page_current = 47
    page_max = get_product()
    get_product()
    # while page_current != page_max:
    #     print('*' * 100)
    #     print('正在爬取第{}页数据'.format(page_current))
    #     print('*' * 100)
    #     new_url = 'https://biotio.en.alibaba.com/productlist-{}.html'.format(page_current)
    #     print(new_url)
    #     driver.get(new_url)  # 拼接url地址
    #     driver.implicitly_wait(2)  # 浏览器等待
    #     page_max = get_product()
    #     page_current += 1

    print("Stop at:", time.asctime(time.localtime(time.time())))


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))

    # 开始
    driver = webdriver.Chrome()
    driver.get('https://biotio.en.alibaba.com/productlist-47.html')
    main()
