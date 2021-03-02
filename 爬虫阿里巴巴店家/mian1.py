# -*- coding: utf-8 -*-
"""
模块：
    1.从配置文件里面拿url,爬取数据，再保存到dianpuData表
    2.检索数据库里面缺失的数据，再补齐。

"""

# 需加检测网页是否加载出来了
import configparser
import threading
import time
import pymongo
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class GetUrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "GetUrl"
        self.config = configparser.ConfigParser()  # 实例化配置文件
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件
        self.url = self.config.get('Parameter', "url")  # 获取店铺主页url

        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_data_col_catalogue": self.config.get("mongoDB", "db_data_col_catalogue"),
            "db_data_col_Data": self.config.get("mongoDB", "db_data_col_Data"),
        }  # 数据库配置
        self.my_client = pymongo.MongoClient(
            self.db_mongoDB["db_url"])  # 实例化数据库
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]  # 实例化库名
        self.db_data_col_catalogue = self.my_db[self.db_mongoDB["db_data_col_catalogue"]]  # 实例化表名
        self.db_data_col_Data = self.my_db[self.db_mongoDB["db_data_col_Data"]]  # 实例化表名

        self.timeSleepExeJsScript = int(
            self.config.get(
                "Parameter",
                "timeSleepExeJsScript"))  # 获取网页休眠时间

        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        with open('C:/Users/18003/AppData/Local/Programs/Python/Python37/stealth.min.js') as f:
            js = f.read()

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        self.driver.maximize_window()

    def run(self):
        print("\n", "*" * 100, sep="\n")
        print("线程：", self.name, "开始")
        try:
            self.driver.get(self.url)
        finally:  # 处理TimeOut，不管有没有加载完成，
            products_Li = self.driver.find_elements_by_xpath('//ul[@class="navigation-list"]/li[2]/div/ul/li')
            for product_Li in products_Li:
                try:  # 一级分类
                    key = product_Li.find_element_by_xpath('./a').get_attribute('title')
                    if "see all" in key.lower():
                        continue
                    val = product_Li.find_element_by_xpath('./a').get_attribute('href')
                    my_data = [{"catalogue_name": key, "category_value": val, }, ]
                    self.db_data_col_catalogue.insert_many(my_data)
                    continue
                except:
                    pass
                try:  # 二级分类
                    key = product_Li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                    products_li = product_Li.find_elements_by_xpath('./div[2]/ul/li')
                    for product_li in products_li:
                        key_erji = key + "---->" + product_li.find_element_by_xpath('./a').get_attribute('title')
                        val_erji = product_li.find_element_by_xpath('./a').get_attribute('href')
                        my_data = [{"catalogue_name": key_erji, "category_value": val_erji, }, ]
                        self.db_data_col_catalogue.insert_many(my_data)
                    continue
                except:
                    pass

                try:  # 三级分类
                    key = product_Li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                    products_li = product_Li.find_elements_by_xpath('./div[2]/ul/li')
                    for product_li in products_li:
                        key_erji = key + "---->" + product_li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                        product_li_c_s = product_li.find_elements_by_xpath('./div[2]/ul/li')
                        for product_li_c in product_li_c_s:
                            key_sanji = key_erji + "---->" + product_li_c.find_element_by_xpath('./a').get_attribute(
                                'title')
                            val_sanji = product_li_c.find_element_by_xpath('./a').get_attribute('href')
                            my_data = [{"catalogue_name": key_sanji, "category_value": val_sanji, }, ]
                            self.db_data_col_catalogue.insert_many(my_data)
                except:
                    pass

            '''
            # 开始爬取url
            '''
            for catalogue_one in self.db_data_col_catalogue.find():
                url = catalogue_one["category_value"]
                self.driver.get(url)
                if len(self.driver.find_elements_by_xpath('//div[@class="module-product-list"]/div')) > 1:
                    FlagA = 1
                    while FlagA == 1:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 使页面加载完毕
                        time.sleep(self.timeSleepExeJsScript)

                        # 16个
                        divss = self.driver.find_elements_by_xpath(
                            '//div[@class="component-product-list"]/div/div[@class="next-row next-row-no-padding '
                            'next-row-no-wrap gallery-view"]')

                        for divs in divss:
                            # 4个：divs_data
                            divs_data = divs.find_elements_by_xpath(
                                './/div[@class="icbu-product-card vertical large product-item"]')
                            try:
                                divs_data.append(divs.find_element_by_xpath(
                                    './/div[@class="icbu-product-card vertical large product-item last"]'))
                            except:
                                pass
                            for div in divs_data:
                                # 共1个
                                url = div.find_element_by_xpath('./a').get_attribute('href')
                                my_data = [
                                    {
                                        "catalogue_name": catalogue_one["catalogue_name"],
                                        "category_value": catalogue_one["category_value"],
                                        "product_url": url,
                                    },
                                ]
                                self.db_data_col_Data.insert_many(my_data)
                        if self.driver.find_element_by_xpath(
                                '//div[@class="next-pagination-pages"]/button[2]').get_attribute('disabled') == 'true':
                            FlagA = 2
                        else:
                            self.driver.find_element_by_xpath('//div[@class="next-pagination-pages"]/button[2]').click()
            self.driver.close()
        print("线程：", self.name, "结束")


class FromUrlGetData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "FromUrlGetData"
        self.config = configparser.ConfigParser()  # 实例化配置文件
        self.config.read("config.ini", encoding="utf-8")  # 读取配置文件

        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_data_col_Data": self.config.get("mongoDB", "db_data_col_Data"),
        }  # 数据库配置
        self.my_client = pymongo.MongoClient(
            self.db_mongoDB["db_url"])  # 实例化数据库
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]  # 实例化库名
        self.db_data_col_Data = self.my_db[self.db_mongoDB["db_data_col_Data"]]  # 实例化表名

        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        with open('C:/Users/18003/AppData/Local/Programs/Python/Python37/stealth.min.js') as f:
            js = f.read()

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        self.driver.maximize_window()

        self.timeSleepExeJsScript = int(
            self.config.get(
                "Parameter",
                "timeSleepExeJsScript"))  # 获取网页休眠时间

        # 初始化数据
        self.product_keywords = ""
        self.product_title = ""
        self.product_mainImageS_middle = []
        self.product_mainImageS = []
        self.product_Overview_dict = {}
        self.product_Overview_dict_middle = []
        self.product_Description = []
        self.product_Description_dict = {}
        self.image_Description = []
        self.images = []
        self.image_Src = ""
        # 等待
        pass

    def run(self):
        print("\n", "*" * 100, sep="\n")
        print("线程：", self.name, "开始")
        time.sleep(30)
        FlagB = 1000
        while FlagB > 0:
            FlagB -= 1
            print(FlagB)
            for url in self.db_data_col_Data.find(no_cursor_timeout=True):
                if "product_url" in url.keys():
                    if "productDescription" not in url.keys():
                        try:
                            print(url)
                            self.driver.get(url["product_url"])
                        finally:  # 处理TimeOut，不管有没有加载完成，都往下处理
                            # 使页面加载完毕
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                            time.sleep(self.timeSleepExeJsScript)
                            self.driver.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
                            time.sleep(self.timeSleepExeJsScript)

                            # 初始化数据
                            self.product_keywords = ""
                            self.product_title = ""
                            self.product_mainImageS_middle = []
                            self.product_mainImageS = []
                            self.product_Overview_dict = {}
                            self.product_Overview_dict_middle = []
                            self.product_Description = []
                            self.product_Description_dict = {}
                            self.image_Description = []
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
                                self.product_mainImageS_middle = self.driver.find_elements_by_xpath(
                                    '//ul[@class="main-image-thumb-ul"]/li')
                            except:
                                pass
                            if not self.product_mainImageS_middle:
                                try:
                                    self.product_mainImageS_middle = self.driver.find_element_by_xpath(
                                        '//ul[@class="main-image-thumb-ul"]/li')
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
                            if not self.product_Description:  # 为空
                                try:
                                    self.product_Description = self.driver.find_elements_by_xpath(
                                        '//div[@class="ife-detail-decorate-table"]/table/tbody/tr')
                                except NoSuchElementException as error:
                                    print("获取网页数据：product Description失败，位置2", error)
                            for elem in self.product_Description:
                                try:
                                    key = elem.find_element_by_xpath('./td[1]').text
                                    val = elem.find_element_by_xpath('./td[2]').text
                                    self.product_Description_dict[key] = val
                                except NoSuchElementException as error:
                                    print("获取网页数据：product Description失败,位置2", error)

                            # 获取网页数据：图片详情
                            try:
                                self.image_Description = self.driver.find_elements_by_xpath(
                                    '//div[@id="J-rich-text-description"]/p')
                            except NoSuchElementException as error:
                                print("获取网页数据：product图片失败，位置1", error)
                            if not self.image_Description:
                                try:
                                    self.image_Description = self.driver.find_elements_by_xpath(
                                        '//div[@id="detail_decorate_root"]/div')
                                except NoSuchElementException as error:
                                    print("获取网页数据：product图片失败，位置2", error)

                            if not self.image_Description:
                                try:
                                    self.image_Description = self.driver.find_elements_by_xpath(
                                        '//div[@id="J-rich-text-description"]/div[2]/p')
                                except NoSuchElementException as error:
                                    print("获取网页数据：product图片失败，位置3", error)

                            if not self.image_Description:
                                try:
                                    self.image_Description = self.driver.find_elements_by_xpath(
                                        '//div[@id="J-rich-text-description"]/div[2]/p')
                                except NoSuchElementException as error:
                                    print("获取网页数据：product图片失败，位置4", error)

                            if not self.image_Description:
                                try:
                                    self.image_Description = self.driver.find_elements_by_xpath(
                                        '//div[@id="J-rich-text-description"]//img')
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

                            # 修改数据
                            my_query = {"product_url": url["product_url"]}
                            new_values = {"$set":
                                {
                                    "keywords": self.product_keywords,
                                    "title": self.product_title,
                                    "mainImage": self.product_mainImageS,
                                    "Overview": self.product_Overview_dict,
                                    "productDescription": self.product_Description_dict,
                                    "imagesDescription": self.images,
                                }
                            }
                            try:
                                self.db_data_col_Data.update_one(my_query, new_values)
                            except:
                                pass
        self.driver.close()
        # 等待
        print("线程：", self.name, "开始")


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
    th = GetUrl()
    th.start()
    thread_list.append(th)

    # 2.从配置文件里面拿url,爬取数据，再保存到dianpuData表中
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
