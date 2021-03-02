# -*- coding: utf-8 -*-  
# 对于从公司名中找不到省市信息的公司访问其网站
import random

import pymongo
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]
mycolprovince_city_PinYin = mydb["province_city_PinYin"]
# 创建表名
mycol3ok_copy = mydb["3ok_copy1"]

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
]
driver = webdriver.Chrome()
driver.set_page_load_timeout(5)
driver.implicitly_wait(5)
def main():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        if 'province' in mycol3ok_copyData.keys() and 'city' in mycol3ok_copyData.keys():
            try:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "http://" + mycol3ok_copyData["website"]
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址","city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)


            except:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "https://" + mycol3ok_copyData["website"]
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)

            else:
                my_query = {"_id": mycol3ok_copyData["_id"]}
                new_values = {"$set": {"province": "http和https访问失败", "city": "http和https访问失败"}}
                mycol3ok_copy.update_one(my_query, new_values)



def mainA():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        if 'province' in mycol3ok_copyData.keys() and 'city' in mycol3ok_copyData.keys():
            try:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "http://" + mycol3ok_copyData["website"] + "/contactus.html"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)


            except:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "https://" + mycol3ok_copyData["website"] + "/contactus.html"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)

            else:
                my_query = {"_id": mycol3ok_copyData["_id"]}
                new_values = {"$set": {"province": "http和https访问失败", "city": "http和https访问失败"}}
                mycol3ok_copy.update_one(my_query, new_values)



def mainB():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        if 'province' in mycol3ok_copyData.keys() and 'city' in mycol3ok_copyData.keys():
            try:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "http://" + mycol3ok_copyData["website"] + "/contact-us.html"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)


            except:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "https://" + mycol3ok_copyData["website"] + "/contact-us.html"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)

            else:
                my_query = {"_id": mycol3ok_copyData["_id"]}
                new_values = {"$set": {"province": "http和https访问失败", "city": "http和https访问失败"}}
                mycol3ok_copy.update_one(my_query, new_values)



def mainC():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        if 'province' in mycol3ok_copyData.keys() and 'city' in mycol3ok_copyData.keys():
            try:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "http://" + mycol3ok_copyData["website"] + "/contactus"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)


            except:
                if mycol3ok_copyData["province"] is None and mycol3ok_copyData["city"] is None:
                    url = "https://" + mycol3ok_copyData["website"] + "/contactus"
                    driver.get(url)
                    htlmStr = driver.page_source
                    FlagA = 1
                    mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
                    for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                        if mycolprovince_city_PinYinData["shiPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                        if mycolprovince_city_PinYinData["shengPinYin"] in htlmStr:
                            my_query = {"_id": mycol3ok_copyData["_id"]}
                            new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                            mycol3ok_copy.update_one(my_query, new_values)
                            FlagA = 2
                    if FlagA == 1:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": "通过html字符串匹配无法找到地址", "city": "通过html字符串匹配无法找到地址"}}
                        mycol3ok_copy.update_one(my_query, new_values)

            else:
                my_query = {"_id": mycol3ok_copyData["_id"]}
                new_values = {"$set": {"province": "http和https访问失败", "city": "http和https访问失败"}}
                mycol3ok_copy.update_one(my_query, new_values)





if __name__ == "__main__":
    print("Start...")
    main()
    mainA()
    mainB()
    mainC()
    pass
