# coding=utf-8

from __future__ import absolute_import
import requests
from lxml import etree
import random
import numpy as np
from time import sleep
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

keyword = sys.argv[1]
url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={}'.format(keyword)
# url = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=mask'


title_url = []
details_list = []
sigel_title1 = []
title_list = []


def make_url():
    # response = requests.get(url)
    # response = response.text
    # list = etree.HTML(response)
    # list1 = list.xpath('//div[@class="list-no-v2-left"]/a/@href')
    # for i in list1:
    #     details_list.append(i[2::])
    # # print(details_list)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo((document.body.scrollHeight)/2, document.body.scrollHeight);")
    time.sleep(2)

    listDiv = driver.find_elements_by_xpath('//div[@class="list-no-v2-left"]/a')
    for list in listDiv:
        title_url.append(list.get_attribute('href'))


def gain_title():
    num_random = np.arange(0, len(title_url))
    random.shuffle(num_random)
    # print(num_random)

    for x in num_random:
        x1 = title_url[x]
        details_response = requests.get(x1)
        details_response = details_response.text
        details_html = etree.HTML(details_response)
        sigel_title = details_html.xpath('//title/text()')

        sigel_title = sigel_title[0].split('-')
        sigel_title = sigel_title[-1]

        sigel_title = sigel_title.split(',')
        # a = ''
        # b = ','
        for i in sigel_title:
            i = i.replace('Product on Alibaba.com', '').replace(u'Buy', '').replace('Hot Sale', '')
            i = i.lstrip()
            if len(i) < 51:
                print(i, '</br>')
        sleep(1)


if __name__ == '__main__':
    make_url()
    gain_title()

