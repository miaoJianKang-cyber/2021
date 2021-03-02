# -*- coding: UTF-8 -*-
import configparser
import time

import pymongo
from selenium import webdriver

# 实例化配置文件
from selenium.common.exceptions import NoSuchElementException

config = configparser.ConfigParser()
# 读取配置文件
config.read("config.ini", encoding="utf-8")
# 从配置文件里加载数据库信息
db_mongoDB = {
    "db_url": config.get("mongoDB", "db_url"),
    "db_client": config.get("mongoDB", "db_client"),
    "db_data_col_Data": config.get("mongoDB", "db_data_col_Data"),
}
# 实例化数据库
my_client = pymongo.MongoClient(db_mongoDB["db_url"])
# 实例化库名
my_db = my_client[db_mongoDB["db_client"]]
# 实例化表名
db_data_col_Data = my_db[db_mongoDB["db_data_col_Data"]]

driver = webdriver.Chrome()

FlagC = 20
FlagB = True
while FlagB:
    FlagC = 20
    for url in db_data_col_Data.find(no_cursor_timeout=True):
        if FlagC > 0:
            if "product_url" in url.keys():
                if "productDescription" not in url.keys():
                    try:
                        print(url["product_url"])
                        driver.execute_script('window.open("' + url["product_url"] + '")')
                    # finally：处理TimeOut，不管有没有加载完成，都往下进行
                    finally:
                        FlagC -= 1
                    FlagB = True
                else:
                    FlagB = False
        else:
            window_list = driver.window_handles.reverse()
            for window_detail in window_list:
                driver.switch_to.window(window_detail)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                time.sleep(1)
            for window_detail in window_list:
                driver.switch_to.window(window_detail)
                driver.execute_script("window.scrollTo((document.body.scrollHeight)/4, (document.body.scrollHeight)*2/4);")
                time.sleep(1)
            for window_detail in window_list:
                driver.switch_to.window(window_detail)
                driver.execute_script("window.scrollTo((document.body.scrollHeight)*2/4, (document.body.scrollHeight)*3/4);")
                time.sleep(1)
            for window_detail in window_list:
                driver.switch_to.window(window_detail)
                driver.execute_script("window.scrollTo((document.body.scrollHeight)*3/4, document.body.scrollHeight);")
                time.sleep(1)
            for window_detail in window_list:
                driver.switch_to.window(window_detail)

                # 初始化商品keywords变量
                product_keywords = ""
                # 初始化商品名称变量
                product_title = ""
                # 初始化商品主图变量1/2
                product_mainImageS_middle = []
                # 初始化商品主图变量2/2
                product_mainImageS = []
                # 初始化商品Overview信息变量1/2
                product_Overview_dict_middle = []
                # 初始化商品Overview信息变量2/2
                product_Overview_dict = {}
                # 初始化商品描述信息变量1/2
                product_Description = []
                # 初始化商品描述信息变量2/2
                product_Description_dict = {}
                # 初始化商品详情图片1/3
                image_Description = []
                # 初始化商品详情图片2/3
                images_Description = []
                # 初始化商品详情图片3/3
                image_Description_Src = ""

                # 获取网页数据：keywords
                try:
                    product_keywords = driver.find_element_by_xpath('//meta[@name="keywords"]').get_attribute('content')
                except BaseException:
                    all_meta = driver.find_elements_by_css_selector('meta')
                    for element_meta in all_meta:
                        if element_meta.get_attribute('name') == 'keywords':
                            product_keywords = element_meta.get_attribute('content')

                # 获取网页数据:title
                try:
                    product_title = driver.find_element_by_class_name('module-pdp-title').get_attribute('title')
                except NoSuchElementException:
                    product_title = driver.find_element_by_class_name('ma-title').get_attribute('title')  # product_title

                # 获取网页数据:Overview
                try:
                    product_Overview_dict_middle = driver.find_elements_by_xpath('//dl[@class="do-entry-item"]')
                except NoSuchElementException:
                    print("获取网页数据：Overview失败，位置1", url)
                for elem in product_Overview_dict_middle:
                    try:
                        key = elem.find_element_by_xpath('./dt').text.replace('.', '')
                        val = elem.find_element_by_xpath('./dd').text
                        product_Overview_dict[key] = val
                    except NoSuchElementException as error:
                        print("获取网页数据：Overview失败，位置2", error)

                # 获取网页数据：主图
                try:
                    product_mainImageS_middle = driver.find_elements_by_xpath('//ul[@class="main-image-thumb-ul"]/li')
                except BaseException:
                    pass
                for elem in product_mainImageS_middle:
                    try:
                        mainImage = elem.find_element_by_xpath('./img').get_attribute('src')
                        product_mainImageS.append(mainImage)
                    except BaseException:
                        pass

                # 获取网页数据：product Description
                try:
                    product_Description = driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]//tr')
                except NoSuchElementException as error:
                    print("获取网页数据：product Description失败，位置1", error)
                for elem in product_Description:
                    try:
                        key = elem.find_element_by_xpath('./td[1]').text
                        val = elem.find_element_by_xpath('./td[2]').text
                        product_Description_dict[key] = val
                    except NoSuchElementException as error:
                        print("获取网页数据：product Description失败,位置2", error)

                # 获取网页数据：图片详情
                try:
                    image_Description = driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]//img')
                except NoSuchElementException as error:
                    print("获取网页数据：product图片失败，位置1", error)
                for elem in image_Description:
                    image_Description_Src = ""
                    try:
                        image_Description_Src = elem.get_attribute("src").replace("_.webp", "")
                    except BaseException:
                        pass
                    if image_Description_Src != "":
                        images_Description.append(image_Description_Src)

                # 修改数据
                my_query = {"product_url": url["product_url"]}
                new_values = {
                    "$set": {
                        "keywords": product_keywords,
                        "title": product_title,
                        "mainImage": product_mainImageS,
                        "Overview": product_Overview_dict,
                        "productDescription": product_Description_dict,
                        "imagesDescription": images_Description,
                    }}
                try:
                    db_data_col_Data.update_one(my_query, new_values)
                except BaseException:
                    pass
driver.close()
