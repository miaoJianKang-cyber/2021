# -*- coding: utf-8 -*-
"""
模块：
    1.从配置文件里面拿url,爬取数据，再保存到dianpuData表
    2.检索数据库里面缺失的数据，再补齐。

"""
import configparser
import os
import shutil
import threading
import time
import pymongo
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from qiniu import Auth, put_file, etag

class GetUrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 线程名称
        self.name = "GetUrl"
        # 实例化配置文件
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read("config.ini", encoding="utf-8")
        # 从配置文件里加载店铺主页url
        self.url = self.config.get('Parameter', "url")  # 获取店铺主页url
        # 从配置文件里加载数据库信息
        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_data_col_catalogue": self.config.get("mongoDB", "db_data_col_catalogue"),
            "db_data_col_Data": self.config.get("mongoDB", "db_data_col_Data"),
        }
        # 实例化数据库
        self.my_client = pymongo.MongoClient(self.db_mongoDB["db_url"])
        # 实例化库名
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]
        # 实例化表名
        self.db_data_col_catalogue = self.my_db[self.db_mongoDB["db_data_col_catalogue"]]
        # 实例化表名
        self.db_data_col_Data = self.my_db[self.db_mongoDB["db_data_col_Data"]]
        # 获取网页休眠时间
        self.timeSleepExeJsScript = int(self.config.get("Parameter", "timeSleepExeJsScript"))
        # 浏览器参数实例化
        self.chrome_options = Options()
        # 增加防反爬参数
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # 实例化浏览器
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # 浏览器运行前执行的js文件：防反爬
        with open('C:/Users/18003/AppData/Local/Programs/Python/Python37/stealth.min.js') as f:
            js = f.read()
        # 浏览器执行js文件
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        # 浏览器最大化
        self.driver.maximize_window()

    def run(self):
        # 输出线程名称：确认哪个线程在执行
        print("*" * 25, "-" * 25, "线程：" + self.name + "开始", "-" * 25, "*" * 25)
        try:
            # 访问店铺主页
            self.driver.get(self.url)
        # 处理TimeOut，不管有没有加载完成
        finally:
            # 获取目录
            # 目录例子：
            '''
            # see all categories
            # Best Seller
            # Medical mask |- Medical protective mask
            #              |- Surgical mask
            # Fancy |- Adult Mask
            #       |- Child Mask
            # Rainbow
            # Civil masks |- Fold masks |- Child Mask
            #                           |- Adult Mask
            #             |- Flat Mask |- Child Mask
            #                          |- Adult Mask
            # Household cleaning tool |- Wipe cloth
            #                         |- Microfiber cloth
            '''
            # products_Li：数据类型：列表，一级目录
            products_Li = self.driver.find_elements_by_xpath('//ul[@class="navigation-list"]/li[2]/div/ul/li')
            # product_Li：数据类型：列表，一级目录里边的每一个条目
            for product_Li in products_Li:
                # 获取该条目
                try:
                    # key：数据类型：字符串，一级目录的名称
                    key = product_Li.find_element_by_xpath('./a').get_attribute('title')
                    # 跳过"see all"
                    if "see all" in key.lower():
                        continue
                    # val:数据类型：字符串，一级目录的名称的url
                    val = product_Li.find_element_by_xpath('./a').get_attribute('href')
                    # catalogue_name:数据类型：字符串，一级目录的名称
                    # catalogue_value:数据类型：字符串，一级目录的名称的url
                    my_data = [{"catalogue_name": key,
                                "catalogue_value": val, }, ]
                    # 一级目录插入数据库
                    self.db_data_col_catalogue.insert_many(my_data)
                    continue
                except BaseException:
                    pass
                # 如果该条目里有二级目录
                try:
                    # key:数据类型：字符串，一级目录的名称，和二级目录一起组成二级目录
                    key = product_Li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                    # products_Li：数据类型：列表，二级目录
                    products_li = product_Li.find_elements_by_xpath('./div[2]/ul/li')
                    # product_Li：数据类型：列表，二级目录里边的每一个
                    for product_li in products_li:
                        # key_erji：数据类型：字符串，二级目录的名称
                        key_erji = key + "---->" + product_li.find_element_by_xpath('./a').get_attribute('title')
                        # val_erji:数据类型：字符串，二级目录的名称的url
                        val_erji = product_li.find_element_by_xpath('./a').get_attribute('href')
                        # catalogue_name:数据类型：字符串，二级目录的名称
                        # catalogue_value:数据类型：字符串，二级目录的名称的url
                        my_data = [{"catalogue_name": key_erji,
                                    "catalogue_value": val_erji, }, ]
                        # 二级目录插入数据库
                        self.db_data_col_catalogue.insert_many(my_data)
                    continue
                except BaseException:
                    pass
                # 如果该条目里有三级级目录
                try:
                    # key:数据类型：字符串，一级目录的名称，和二级、三级目录一起组成三级目录
                    key = product_Li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                    # products_Li：数据类型：列表，三级目录
                    products_li = product_Li.find_elements_by_xpath('./div[2]/ul/li')
                    # product_Li：数据类型：列表，二级目录里边的每一个
                    for product_li in products_li:
                        # key_erji：数据类型：字符串，二级目录的名称
                        key_erji = key + "---->" + product_li.find_element_by_xpath('./div[1]/a').get_attribute('title')
                        # product_li_c_s：数据类型：列表，三级目录里边的每一个
                        product_li_c_s = product_li.find_elements_by_xpath('./div[2]/ul/li')
                        # product_li_c：三级目录里的每一个
                        for product_li_c in product_li_c_s:
                            # key_sanji：数据类型：字符串，三级目录的名称
                            key_sanji = key_erji + "---->" + product_li_c.find_element_by_xpath('./a').get_attribute('title')
                            # val_sanji:数据类型：字符串，三级目录的名称的url
                            val_sanji = product_li_c.find_element_by_xpath('./a').get_attribute('href')
                            # catalogue_name:数据类型：字符串，三级目录的名称
                            # catalogue_value:数据类型：字符串，三级目录的名称的url
                            my_data = [{"catalogue_name": key_sanji,
                                        "catalogue_value": val_sanji, }, ]
                            # 三级目录插入数据库
                            self.db_data_col_catalogue.insert_many(my_data)
                except BaseException:
                    pass

            # 开始爬取url
            # self.db_data_col_catalogue.find()：获取所有目录
            # catalogue_one：目录中的一个
            for catalogue_one in self.db_data_col_catalogue.find():
                # 获取商品展示url
                url = catalogue_one["catalogue_value"]
                # 访问商品展示url
                self.driver.get(url)
                # 如果有商品
                if len(self.driver.find_elements_by_xpath('//div[@class="module-product-list"]/div')) > 1:
                    # FlagA：数据类型：bool,判断是否市最后一页
                    FlagA = True
                    while FlagA:
                        # 滑动滚轮到底，使页面加载完毕
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                        time.sleep(self.timeSleepExeJsScript)
                        self.driver.execute_script("window.scrollTo(document.body.scrollHeight/3, (document.body.scrollHeight)*2/3);")
                        time.sleep(self.timeSleepExeJsScript)
                        self.driver.execute_script("window.scrollTo((document.body.scrollHeight)*2/3, document.body.scrollHeight);")
                        time.sleep(self.timeSleepExeJsScript)

                        # 全部商品标签（共四层，每层四个），列表divss的长度是4，表示4层
                        divss = self.driver.find_elements_by_xpath(
                            '//div[@class="component-product-list"]/div/div[@class="next-row next-row-no-padding '
                            'next-row-no-wrap gallery-view"]')
                        # 每层商品标签
                        for divs in divss:
                            # divs_data：商品标签，每层中的商品，长度一般是4，如果是最后一层也可能是1、2或者3
                            divs_data = divs.find_elements_by_xpath('.//div[@class="icbu-product-card vertical large product-item"]')
                            # 每层商品的最后一个class属性特殊，所以需要单独找到再加入每层列表中
                            try:
                                divs_data.append(divs.find_element_by_xpath('.//div[@class="icbu-product-card vertical large product-item last"]'))
                            except BaseException:
                                pass
                            # div：每个商品的标签
                            for div in divs_data:
                                # 数据类型：字符串，每个商品的url
                                url = div.find_element_by_xpath('./a').get_attribute('href')
                                # catalogue_name：商品所在的目录
                                # catalogue_value：商品所在的目录展示页面
                                # product_url：商品的url，到这里这个类的作用就结束了
                                my_data = [
                                    {
                                        "catalogue_name": catalogue_one["catalogue_name"],
                                        "catalogue_value": catalogue_one["catalogue_value"],
                                        "product_url": url,
                                    },
                                ]
                                # 商品信息插入数据库
                                self.db_data_col_Data.insert_many(my_data)
                        # 翻页功能：如果商品展示页是多页就一页一页的翻
                        if self.driver.find_element_by_xpath('//div[@class="next-pagination-pages"]/button[2]').get_attribute('disabled') == 'true':
                            FlagA = False
                        else:
                            self.driver.find_element_by_xpath('//div[@class="next-pagination-pages"]/button[2]').click()
            self.driver.close()
        # 输出线程名称：确认哪个线程在执行
        print("*" * 25, "-" * 25, "线程：" + self.name + "结束", "-" * 25, "*" * 25)


class FromUrlGetData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 线程名称
        self.name = "FromUrlGetData"
        # 实例化配置文件
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read("config.ini", encoding="utf-8")
        # 从配置文件里加载数据库信息
        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_data_col_Data": self.config.get("mongoDB", "db_data_col_Data"),
        }
        # 实例化数据库
        self.my_client = pymongo.MongoClient(self.db_mongoDB["db_url"])
        # 实例化库名
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]
        # 实例化表名
        self.db_data_col_Data = self.my_db[self.db_mongoDB["db_data_col_Data"]]
        # 浏览器参数实例化
        self.chrome_options = Options()
        # 增加防反爬参数
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # 实例化浏览器
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # 浏览器运行前执行的js文件：防反爬
        with open('C:/Users/18003/AppData/Local/Programs/Python/Python37/stealth.min.js') as f:
            js = f.read()
        # 浏览器执行js文件
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })
        # 浏览器最大化
        self.driver.maximize_window()
        # 获取网页休眠时间
        self.timeSleepExeJsScript = int(self.config.get("Parameter", "timeSleepExeJsScript"))

        # 定义商品keywords变量
        self.product_keywords = ""
        # 定义商品名称变量
        self.product_title = ""
        # 定义商品主图变量1/2
        self.product_mainImageS_middle = []
        # 定义商品主图变量2/2
        self.product_mainImageS = []
        # 定义商品Overview信息变量1/2
        self.product_Overview_dict_middle = []
        # 定义商品Overview信息变量2/2
        self.product_Overview_dict = {}
        # 定义商品描述信息变量1/2
        self.product_Description = []
        # 定义商品描述信息变量2/2
        self.product_Description_dict = {}
        # 定义商品详情图片1/3
        self.image_Description = []
        # 定义商品详情图片2/3
        self.images_Description = []
        # 定义商品详情图片3/3
        self.image_Description_Src = ""

    def run(self):
        # 输出线程名称：确认哪个线程在执行
        print("*" * 25, "-" * 25, "线程：" + self.name + "开始", "-" * 25, "*" * 25)

        FlagB = True
        while FlagB:
            for url in self.db_data_col_Data.find(no_cursor_timeout=True):
                if "product_url" in url.keys():
                    if "productDescription" not in url.keys():
                        try:
                            print(url["product_url"])
                            self.driver.get(url["product_url"])
                        # finally：处理TimeOut，不管有没有加载完成，都往下进行
                        finally:
                            # 使页面加载完毕
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                            time.sleep(self.timeSleepExeJsScript)
                            self.driver.execute_script("window.scrollTo((document.body.scrollHeight)/4, (document.body.scrollHeight)*2/4);")
                            time.sleep(self.timeSleepExeJsScript)
                            self.driver.execute_script("window.scrollTo((document.body.scrollHeight)*2/4, (document.body.scrollHeight)*3/4);")
                            time.sleep(self.timeSleepExeJsScript)
                            self.driver.execute_script("window.scrollTo((document.body.scrollHeight)*3/4, document.body.scrollHeight);")
                            time.sleep(self.timeSleepExeJsScript + 1)

                            # 初始化商品keywords变量
                            self.product_keywords = ""
                            # 初始化商品名称变量
                            self.product_title = ""
                            # 初始化商品主图变量1/2
                            self.product_mainImageS_middle = []
                            # 初始化商品主图变量2/2
                            self.product_mainImageS = []
                            # 初始化商品Overview信息变量1/2
                            self.product_Overview_dict_middle = []
                            # 初始化商品Overview信息变量2/2
                            self.product_Overview_dict = {}
                            # 初始化商品描述信息变量1/2
                            self.product_Description = []
                            # 初始化商品描述信息变量2/2
                            self.product_Description_dict = {}
                            # 初始化商品详情图片1/3
                            self.image_Description = []
                            # 初始化商品详情图片2/3
                            self.images_Description = []
                            # 初始化商品详情图片3/3
                            self.image_Description_Src = ""

                            # 获取网页数据：keywords
                            try:
                                self.product_keywords = self.driver.find_element_by_xpath('//meta[@name="keywords"]').get_attribute('content')
                            except BaseException:
                                all_meta = self.driver.find_elements_by_css_selector('meta')
                                for element_meta in all_meta:
                                    if element_meta.get_attribute('name') == 'keywords':
                                        self.product_keywords = element_meta.get_attribute('content')

                            # 获取网页数据:title
                            try:
                                self.product_title = self.driver.find_element_by_class_name('module-pdp-title').get_attribute('title')
                            except NoSuchElementException:
                                self.product_title = self.driver.find_element_by_class_name('ma-title').get_attribute('title')  # product_title

                            # 获取网页数据:Overview
                            try:
                                self.product_Overview_dict_middle = self.driver.find_elements_by_xpath('//dl[@class="do-entry-item"]')
                            except NoSuchElementException:
                                print("获取网页数据：Overview失败，位置1", url)
                            for elem in self.product_Overview_dict_middle:
                                try:
                                    key = elem.find_element_by_xpath('./dt').text.replace('.', '')
                                    val = elem.find_element_by_xpath('./dd').text
                                    self.product_Overview_dict[key] = val
                                except NoSuchElementException as error:
                                    print("获取网页数据：Overview失败，位置2", error)

                            # 获取网页数据：主图
                            try:
                                self.product_mainImageS_middle = self.driver.find_elements_by_xpath('//ul[@class="main-image-thumb-ul"]/li')
                            except BaseException:
                                pass
                            for elem in self.product_mainImageS_middle:
                                try:
                                    mainImage = elem.find_element_by_xpath('./img').get_attribute('src')
                                    self.product_mainImageS.append(mainImage)
                                except BaseException:
                                    pass

                            # 获取网页数据：product Description
                            try:
                                self.product_Description = self.driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]//tr')
                            except NoSuchElementException as error:
                                print("获取网页数据：product Description失败，位置1", error)
                            for elem in self.product_Description:
                                try:
                                    key = elem.find_element_by_xpath('./td[1]').text
                                    val = elem.find_element_by_xpath('./td[2]').text
                                    self.product_Description_dict[key] = val
                                except NoSuchElementException as error:
                                    print("获取网页数据：product Description失败,位置2", error)

                            # 获取网页数据：图片详情
                            try:
                                self.image_Description = self.driver.find_elements_by_xpath('//div[@id="J-rich-text-description"]//img')
                            except NoSuchElementException as error:
                                print("获取网页数据：product图片失败，位置1", error)
                            for elem in self.image_Description:
                                self.image_Description_Src = ""
                                try:
                                    self.image_Description_Src = elem.get_attribute("src").replace("_.webp", "")
                                except BaseException:
                                    pass
                                if self.image_Description_Src != "":
                                    self.images_Description.append(self.image_Description_Src)

                            # 修改数据
                            my_query = {"product_url": url["product_url"]}
                            new_values = {
                                "$set": {
                                    "keywords": self.product_keywords,
                                    "title": self.product_title,
                                    "mainImage": self.product_mainImageS,
                                    "Overview": self.product_Overview_dict,
                                    "productDescription": self.product_Description_dict,
                                    "imagesDescription": self.images_Description,
                                }}
                            try:
                                self.db_data_col_Data.update_one(my_query, new_values)
                            except BaseException:
                                pass
                        FlagB = True
                    else:
                        FlagB = False
        self.driver.close()
        print("*" * 25, "-" * 25, "线程：" + self.name + "结束", "-" * 25, "*" * 25)

space2url = {
            "xinhaitui": "http://qp2bm1bf4.hn-bkt.clouddn.com"
        }

def up2qiniu(local_img, space_name, img_name):
    access_key = '9NOdpqP-j_RWKsmDyJ9UGau08sFDfpSbULVnCT6F'
    secret_key = 'x-h8gpjwWIRbzk_dqzO3tk3GOy1yQAGw-UK6OUEm'
    q = Auth(access_key, secret_key)  # 构建鉴权对象
    bucket_name = space_name  # 要上传的空间
    key = img_name  # 上传后保存的文件名
    token = q.upload_token(bucket_name, key, 3600)  # 生成上传 Token，可以指定过期时间等
    localfile = local_img  # 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    img_url = urljoin(space2url[space_name], img_name)
    return img_url

class FromImageUrlGet7NiuYunUrl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "FromImageUrlGet7NiuYunUrl"
        # 实例化配置文件
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read("config.ini", encoding="utf-8")
        # 从配置文件里加载数据库信息
        self.db_mongoDB = {
            "db_url": self.config.get("mongoDB", "db_url"),
            "db_client": self.config.get("mongoDB", "db_client"),
            "db_data_col_Data": self.config.get("mongoDB", "db_data_col_Data"),
        }
        # 实例化数据库
        self.my_client = pymongo.MongoClient(self.db_mongoDB["db_url"])
        # 实例化库名
        self.my_db = self.my_client[self.db_mongoDB["db_client"]]
        # 实例化表名
        self.db_data_col_Data = self.my_db[self.db_mongoDB["db_data_col_Data"]]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

        self.imagesDescription_7niuyun = []
        self.mainImage_7niuyun = []

    def run(self):
        # 输出线程名称：确认哪个线程在执行
        print("*" * 25, "-" * 25, "线程：" + self.name + "开始", "-" * 25, "*" * 25)
        if not os.path.exists('images'):
            os.mkdir('images')
        FlagC = True
        while FlagC:
            time.sleep(60)
            for url in self.db_data_col_Data.find(no_cursor_timeout=True):
                if "imagesDescription" in url.keys():
                    if "imagesDescription_7niuyun" not in url.keys():
                        self.imagesDescription_7niuyun = []
                        for image_url in url["imagesDescription"]:
                            print(image_url)
                            image_name = image_url.split('/')[-2] + image_url.split('/')[-1]
                            image_path = 'images/' + image_name
                            image_data = requests.get(url=image_url, headers=self.headers).content
                            with open(image_path, 'wb') as fp:
                                fp.write(image_data)
                            res = up2qiniu(image_path, "xinhaitui", image_name)
                            self.imagesDescription_7niuyun.append(res)
                        # 修改数据
                        my_query = {"imagesDescription": url["imagesDescription"]}
                        new_values = {
                            "$set": {
                                "imagesDescription_7niuyun": self.imagesDescription_7niuyun,
                            }}
                        try:
                            self.db_data_col_Data.update_one(my_query, new_values)
                        except BaseException:
                            pass
                        FlagC = True
                    else:
                        FlagC = False

                if "mainImage" in url.keys():
                    if "mainImage_7niuyun" not in url.keys():
                        self.mainImage_7niuyun = []
                        for image_url in url["mainImage"]:
                            print(image_url)
                            image_name = image_url.split('/')[-2] + image_url.split('/')[-1]
                            image_path = 'images/' + image_name
                            image_data = requests.get(url=image_url, headers=self.headers).content
                            with open(image_path, 'wb') as fp:
                                fp.write(image_data)
                            res = up2qiniu(image_path, "xinhaitui", image_name)
                            self.mainImage_7niuyun.append(res)
                        # 修改数据
                        my_query = {"mainImage": url["mainImage"]}
                        new_values = {
                            "$set": {
                                "mainImage_7niuyun": self.mainImage_7niuyun,
                            }}
                        try:
                            self.db_data_col_Data.update_one(my_query, new_values)
                        except BaseException:
                            pass
                        FlagC = True
                    else:
                        FlagC = False
        shutil.rmtree("images")
        print("*" * 25, "-" * 25, "线程：" + self.name + "结束", "-" * 25, "*" * 25)


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

    # 3.把阿里巴巴图片链接换成7牛云链接
    th = FromImageUrlGet7NiuYunUrl()
    th.start()
    thread_list.append(th)

    # 协调线程
    for th in thread_list:
        th.join()
