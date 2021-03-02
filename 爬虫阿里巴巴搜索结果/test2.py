# -*- coding: UTF-8 -*-

# 奖列表分成n份
import math
import time

from bs4 import BeautifulSoup
from selenium import webdriver
images = []
if not images :
        print("ok")

driver = webdriver.Chrome()
driver.maximize_window()

# 三.打开列表网页
driver.get("https://www.alibaba.com/product-detail/Mask-Mask-3-Ply-Surgical-Mask_1600137181426.html?s=p&bypass=true")
driver.execute_script('window.scrollBy(0,10000)')  # 使页面加载完毕
time.sleep(4)

try:
        image_Description = driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]/p')
except:
        image_Description = driver.find_elements_by_xpath('//div[@id="detail_decorate_root"]/div')




image_Description = driver.find_elements_by_xpath('//div[@id="detail_decorate_root"]/div')

# html = driver.page_source
# soup = BeautifulSoup(html, 'lxml')
#
# images_div = soup.find_all('div', {'id': 'detail_decorate_root'})
# print(images_div)
# for child in images_div.descendants:
#     print(child)
src = ""
for elem in image_Description:
        try:
                src = elem.find_element_by_tag_name('img').get_attribute("src")
        except:
                pass
        if src != "":
                images.append(src)
print(images)


