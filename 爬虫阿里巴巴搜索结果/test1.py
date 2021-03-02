# -*- coding: UTF-8 -*-

# 奖列表分成n份
import math

import requests
from selenium import webdriver

driver = webdriver.Chrome()
product_info_dict = {}
# 三.打开列表网页
driver.get(
    "https://www.alibaba.com/product-detail/Mask-Hot-sell-Disposable-Elastic-Medical_1600146057146.html?spm=a2700.galleryofferlist.normal_offer.d_image.40a0135eCIbcPi&s=p")
main_image_elems = driver.find_elements_by_class_name("main-image-thumb-item")
for main_image_url in main_image_elems:
    img_url = main_image_url.find_element_by_xpath("./img").get_attribute("src")
    response = requests.get(img_url)

    with open("img.jpg", 'wb') as f:
        f.write(response.content)
    f.close()


    pass
