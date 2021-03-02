# -*- coding: utf-8 -*-
"""
模块：
    1.获取url,保存到数据库里面
    2.从数据库里面拿url,爬取数据，再保存到url
    3.检索数据库里面缺失的数据，再补齐。

"""

# 需加检测网页是否加载出来了
import configparser
import threading
import time
import pymongo
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class GetUrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "GetUrl"
        self.config = configparser.ConfigParser()  # 实例化配置文件
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件

        self.keyword = self.config.get('Parameter', "keyword")  # 获取关键字
        self.url = self.config.get("Parameter",
                                   "url") + self.keyword  # 获取url
        self.number = int(self.config.get("Parameter", "number"))  # 获取数量
        self.address = self.config.get("Parameter", "address")  # 获取保存地址
        self.jsScript = self.config.get("Parameter", "jsScript")  # 获取网页高度
        self.timeSleepExeJsScript = int(
            self.config.get(
                "Parameter",
                "timeSleepExeJsScript"))  # 获取网页休眠时间
        self.js = 'window.scrollBy(0,' + self.jsScript + ')'

        self.chrome_options = webdriver.ChromeOptions()  # 配置浏览器
        self.chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.driver = webdriver.Chrome()

        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_urls_col": self.config.get("mongoDB", "db_urls_col")
        }  # 数据库配置

        self.my_client = pymongo.MongoClient(
            self.db_mongoDB["db_url"])  # 实例化数据库
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]  # 实例化库名
        self.my_urls_col = self.my_db[self.db_mongoDB["db_urls_col"]]  # 实例化表名
        self.my_urls_col.delete_many({})  # 清理旧数据
        # 等待
        pass

    def run(self):
        print("\n", "*" * 100, sep="\n")
        print("线程：", self.name)
        print(
            "url：" + self.url,
            "读取个数: " + str(self.number),
            "保存地址: " + self.address,
            sep="\n")

        self.driver.get(self.url)
        self.driver.execute_script(self.js)  # 使页面加载完毕
        time.sleep(self.timeSleepExeJsScript)
        self.driver.execute_script(self.js)  # 使页面加载完毕
        productWebelems = self.driver.find_elements_by_class_name(
            "list-no-v2-left")
        if len(productWebelems) > self.number:
            productWebelems = productWebelems[:self.number]
            for i in productWebelems:
                try:
                    url = i.find_element_by_class_name(
                        "list-no-v2-left__img-container").get_attribute("href")
                    my_data = [{
                        "keyword": self.keyword,
                        "url": self.url,
                        "urlResult": url
                    }]
                    self.my_urls_col.insert_many(my_data)
                except NoSuchElementException:
                    # print("获取url失败一次！")
                    pass
        else:
            # --------------------------------------------------------- #
            for i in productWebelems:
                try:
                    url = i.find_element_by_class_name(
                        "list-no-v2-left__img-container").get_attribute("href")
                    my_data = [{
                        "keyword": self.keyword,
                        "url": self.url,
                        "urlResult": url
                    }]
                    self.my_urls_col.insert_many(my_data)
                except NoSuchElementException:
                    # print("获取url失败一次！")
                    pass
            self.number = self.number - len(productWebelems)
            # --------------------------------------------------------- #
            page_num = 2
            while self.number > 0:
                page_url = "https://www.alibaba.com/products/" + self.keyword + \
                           ".html?IndexArea=product_en&page=" + str(page_num)
                page_num += 1
                self.driver.get(page_url)
                self.driver.execute_script(self.js)  # 使页面加载完毕
                time.sleep(self.timeSleepExeJsScript)
                self.driver.execute_script(self.js)  # 使页面加载完毕
                productWebelems = self.driver.find_elements_by_class_name(
                    "list-no-v2-left")
                for i in productWebelems:
                    try:
                        url = i.find_element_by_class_name(
                            "list-no-v2-left__img-container").get_attribute("href")
                        my_data = [{
                            "keyword": self.keyword,
                            "url": self.url,
                            "urlResult": url
                        }]
                        self.my_urls_col.insert_many(my_data)
                        self.number = self.number - 1
                        if self.number == 0:
                            break
                    except NoSuchElementException:
                        # print("获取url失败一次！")
                        pass

        self.driver.close()
        # 等待
        pass


class FromUrlGetData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "FromUrlGetData"
        self.config = configparser.ConfigParser()  # 实例化配置文件
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件
        self.keyword = self.config.get('Parameter', "keyword")  # 获取关键字

        self.chrome_options = webdriver.ChromeOptions()  # 配置浏览器
        # self.chrome_options.add_argument('--headless') # 无界面模式
        self.chrome_options.add_argument("--proxy-server=http://220.249.149.11:9999")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window()

        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_urls_col": self.config.get("mongoDB", "db_urls_col"),
            "db_data_col": self.config.get("mongoDB", "db_data_col")
        }  # 数据库配置

        self.jsScript = self.config.get("Parameter", "jsScript")  # 获取网页高度
        self.timeSleepExeJsScript = int(
            self.config.get(
                "Parameter",
                "timeSleepExeJsScript"))  # 获取网页休眠时间
        self.js = 'window.scrollBy(0,' + self.jsScript + ')'

        self.my_client = pymongo.MongoClient(
            self.db_mongoDB["db_url"])  # 实例化数据库
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]  # 实例化库名
        self.db_urls_col = self.my_db[self.db_mongoDB["db_urls_col"]]  # 实例化表名
        self.db_data_col = self.my_db[self.db_mongoDB["db_data_col"]]  # 实例化表名

        # 初始化数据
        self.product_keywords = ""
        self.product_title = ""
        self.product_mainImageS_middle = ""
        self.product_mainImageS = []
        self.product_Overview_dict = {}
        self.product_Overview_dict_middle = ""
        self.product_Description = ""
        self.product_Description_dict = {}
        self.image_Description = ""
        self.images = []
        self.image_Src = ""
        # 等待

    def run(self):
        print("\n", "*" * 100, sep="\n")
        print("线程：", self.name)
        for url in self.db_urls_col.find():
            print(url["urlResult"])
            try:
                self.driver.get(url["urlResult"])
            finally:  # 处理TimeOut，不管有没有加载完成，都往下处理
                # if url["urlResult"] == self.driver.current_url:  # 检查页面是否加载出来了
                self.driver.maximize_window()
                self.driver.execute_script(self.js)  # 使页面加载完毕
                time.sleep(self.timeSleepExeJsScript)
                self.driver.execute_script(self.js)  # 使页面加载完毕
                time.sleep(self.timeSleepExeJsScript / 2)

                # 初始化数据
                self.product_keywords = ""
                self.product_title = ""
                self.product_mainImageS_middle = ""
                self.product_mainImageS = []
                self.product_Overview_dict = {}
                self.product_Overview_dict_middle = ""
                self.product_Description = ""
                self.product_Description_dict = {}
                self.image_Description = ""
                self.images = []
                self.image_Src = ""

                # 获取网页数据：keywords
                try:
                    self.product_keywords = self.driver.find_element_by_xpath(
                        '//meta[@name="keywords"]').get_attribute('content')
                except BaseException:
                    all_meta = self.driver.find_elements_by_css_selector('meta')
                    for element_meta in all_meta:
                        if element_meta.get_attribute('name') == 'keywords':
                            self.product_keywords = element_meta.get_attribute(
                                'content')
                            continue
                try:
                    if self.product_keywords == "":
                        self.product_keywords = self.driver.find_element_by_xpath(
                            '/html/head/meta[2]').get_attribute('content')
                except BaseException:
                    pass

                # 获取网页数据:title
                try:
                    self.product_title = self.driver.find_element_by_class_name(
                        'module-pdp-title').get_attribute('title')  # product_title
                except NoSuchElementException:
                    self.product_title = self.driver.find_element_by_class_name(
                        'ma-title').get_attribute('title')  # product_title
                # 获取网页数据:Overview
                try:
                    self.product_Overview_dict_middle = self.driver.find_elements_by_xpath(
                        '//dl[@class="do-entry-item"]')
                except NoSuchElementException:
                    print("获取网页数据：Overview失败，位置1", url)
                for elem in self.product_Overview_dict_middle:
                    try:
                        key = elem.find_element_by_xpath(
                            './dt').text.replace('.', '')
                        val = elem.find_element_by_xpath('./dd').text
                        self.product_Overview_dict[key] = val
                    except NoSuchElementException as error:
                        print("获取网页数据：Overview失败，位置2", error)

                # 获取网页数据：主图
                try:
                    self.product_mainImageS_middle = self.driver.find_elements_by_xpath('//ul[@class="main-image-thumb-ul"]/li')
                except:
                    pass
                for elem in self.product_mainImageS_middle:
                    try:
                        mainImage = elem.find_element_by_xpath('./img').get_attribute('src')
                        self.product_mainImageS.append(mainImage)
                    except:
                        pass


                # 获取网页数据：product Description
                try:
                    self.product_Description = self.driver.find_elements_by_xpath(
                        '//div[@id="J-rich-text-description"]/table/tbody/tr')
                except NoSuchElementException as error:
                    print("获取网页数据：product Description失败，位置1", error)
                    pass
                for elem in self.product_Description:
                    try:
                        key = elem.find_element_by_xpath('./td[1]').text
                        val = elem.find_element_by_xpath('./td[2]').text
                        self.product_Description_dict[key] = val
                    except NoSuchElementException as error:
                        print("获取网页数据：product Description失败,位置2", error)

                # 获取网页数据：图片
                try:
                    self.image_Description = self.driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]/p')
                except NoSuchElementException as error:
                    print("获取网页数据：product图片失败，位置1", error)
                if not self.image_Description:
                    try:
                        self.image_Description = self.driver.find_elements_by_xpath('//div[@id="detail_decorate_root"]/div')
                    except NoSuchElementException as error:
                        print("获取网页数据：product图片失败，位置2", error)

                if not self.image_Description:
                    try:
                        self.image_Description = self.driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]/div[2]/p')
                    except NoSuchElementException as error:
                        print("获取网页数据：product图片失败，位置3", error)

                if not self.image_Description:
                    try:
                        self.image_Description = self.driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]//div[1]/div[2]/p')
                    except NoSuchElementException as error:
                        print("获取网页数据：product图片失败，位置4", error)



                for elem in self.image_Description:
                    self.image_Src = ""
                    try:
                        self.image_Src = elem.find_element_by_tag_name('img').get_attribute("src")
                    except:
                        pass
                    if self.image_Src != "":
                        self.images.append(self.image_Src)



                # 保存数据
                my_data = [
                    {
                        "_id": time.strftime(
                            "%Y-%m-%d %H:%M:%S",
                            time.localtime()),
                        "keyword": self.keyword,
                        "keywords": self.product_keywords,
                        "url": url["urlResult"],
                        "title": self.product_title,
                        "mainImage":self.product_mainImageS,
                        "Overview": self.product_Overview_dict,
                        "productDescription": self.product_Description_dict,
                        "imagesDescription": self.images,
                    },
                ]
                self.db_data_col.insert_many(my_data)
        self.driver.close()
        # 等待
        pass


class CheckData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "CheckData"
        # 等待
        pass

    def run(self):
        print("\n", "*" * 100, sep="\n")
        print("线程：", self.name)
        # 等待
        pass


if __name__ == '__main__':

    # 线程存放列表
    thread_list = []

    # 1.获取url,保存到数据库里面
    # th = GetUrl()
    # th.start()
    # thread_list.append(th)

    # 2.从数据库里面拿url,爬取数据，再保存到url
    th = FromUrlGetData()
    th.start()
    thread_list.append(th)

    # 3.检索数据库里面缺失的数据，再补齐。
    # th = CheckData()
    # th.start()
    # thread_list.append(th)

    # 协调线程
    for th in thread_list:
        th.join()
