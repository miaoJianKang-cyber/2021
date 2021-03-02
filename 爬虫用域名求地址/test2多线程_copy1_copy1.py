# -*- coding: UTF-8 -*-

import threading
import time

import pymongo
import pymysql
import requests  # 替代浏览器发送网络请求
from bs4 import BeautifulSoup
from selenium import webdriver

# pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycolPinYin = mydb["province_city_PinYin"]
mycol3ok_copy = mydb["3ok_copy1"]

mongodb3ok_copyDatas = mycol3ok_copy.find()
mongodbPinYinDatas = mycolPinYin.find()

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/537.36',

}

lock = threading.Lock()
lock1 = threading.Lock()

data_list = []
for data in mongodb3ok_copyDatas:
    if data["province"] is None and data["city"] is None:
        data_list.append(data)
    pass




def get_data_list():
    global data_list
    list_copy = data_list[0]
    data_list.remove(data_list[0])
    return list_copy


class myThread(threading.Thread):
    def __init__(self, threadId):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.flagStatusCode = False

    def run(self):
        # driver = webdriver.Chrome()
        # driver.maximize_window()
        for i in range(0, 20):
            lock1.acquire()
            data = get_data_list()
            lock1.release()
            print(data["website"])

            url = data["website"]
            if "www" not in url:
                url = "www." + url
            try:
                r = requests.get(url,headers=headers)
                if r.status_code == 200:
                    self.flagStatusCode = True
                    pass
            except:
                urlResult = requests.get("http://" + url, headers=headers)
                if urlResult.status_code == 200:
                    self.flagStatusCode = True
                    pass

            else:
                urlsResult = requests.get("https://" + url, headers=headers)
                if urlsResult.status_code == 200:
                    self.flagStatusCode = True
                    pass
            if self.flagStatusCode == False:
                myquery = {"website": data["website"]}
                newvalues = {"$set": {"province": "主页打不开"}}
                mycol3ok_copy.update_one(myquery, newvalues)
            # try:
            #     r = requests.get(url, headers=headers)
            #     if r.status_code == 200:
            #         try:
            #             url = "http://" + str(data[2]) + "/contact-us"
            #             driver.get(url)
            #             html = driver.page_source
            #             soup = BeautifulSoup(html, 'lxml')
            #             elem_data = soup.prettify()
            #             # print(type(elem_data))
            #             # 打开一个文件
            #             fo = open("elements" + str(self.threadId) + ".txt", "w", encoding='utf-8')
            #             fo.write(elem_data)
            #             # 关闭打开的文件
            #             fo.close()
            #
            #             # 打开文件
            #             fo = open("elements" + str(self.threadId) + ".txt", "r", encoding="utf-8")
            #             sql_update = ""
            #             for line in fo.readlines():  # 依次读取每行
            #                 line = line.strip().lower()  # 去掉每行头尾空白和全部转为小写
            #
            #                 for mongodbData in mongodbDatas:
            #                     print(mongodbData)
            #                     print(mongodbData["shengPinYin"])
            #                     print(mongodbData["sheng"])
            #                     print(mongodbData["shiPinYin"])
            #                     print(mongodbData["shi"])
            #                     if mongodbData["shengPinYin"] in line: # 有省
            #                         sql_update = "UPDATE 3ok_copy1 SET province = "+ mongodbData["sheng"] +" WHERE website = '" + data[2] + "';"
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(sql_update)
            #                         # 提交修改
            #                         conn.commit()
            #                         lock.release()
            #                     else:# 没省
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute("UPDATE 3ok_copy1 SET province = '本网站未显示地址' WHERE website = '" + data[2] + "';")
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #
            #                     if mongodbData["shiPinYin"] in line: # 有市
            #                         sql_update = "UPDATE 3ok_copy1 SET city = "+ mongodbData["shi"] +" WHERE website = '" + data[2] + "';"
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(sql_update)
            #                         # 提交修改
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #                     else: # 没市
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute("UPDATE 3ok_copy1 SET city = '本网站未显示地址' WHERE website = '" + data[2] + "';")
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #             fo.close()
            #         except:
            #             print("子网址打不开：", url)
            #             sql_update = "UPDATE 3ok_copy1 SET province = 'contact-us网址打不开' WHERE website = '" + data[
            #                 2] + "';"
            #             conn.ping(reconnect=True)
            #             lock.acquire()
            #             cur.execute(sql_update)
            #             conn.commit()
            #             lock.release()
            # except:
            #     print("主网站打不开:", url)
            #     sql_update = "UPDATE 3ok_copy1 SET city = '主网站打不开' WHERE website = '" + data[2] + "';"
            #     conn.ping(reconnect=True)
            #     lock.acquire()
            #     cur.execute(sql_update)
            #     conn.commit()
            #     lock.release()
            #
            # # https
            # urls = "https://" + str(data[2])
            # try:
            #     r = requests.get(urls, headers=headers)
            #     if r.status_code == 200:
            #         try:
            #             urls = "https://" + str(data[2]) + "/contact-us"
            #             driver.get(urls)
            #             html = driver.page_source
            #             soup = BeautifulSoup(html, 'lxml')
            #             elem_data = soup.prettify()
            #             # print(type(elem_data))
            #             # 打开一个文件
            #             fo = open("elements" + str(self.threadId) + ".txt", "w", encoding='utf-8')
            #             fo.write(elem_data)
            #             # 关闭打开的文件
            #             fo.close()
            #
            #             # 打开文件
            #             fo = open("elements" + str(self.threadId) + ".txt", "r", encoding="utf-8")
            #             sql_update = ""
            #             for line in fo.readlines():  # 依次读取每行
            #                 line = line.strip().lower()  # 去掉每行头尾空白和全部转为小写
            #
            #                 for mongodbData in mongodbDatas:
            #                     if mongodbData["shengPinYin"] in line:  # 有省
            #                         sql_update = "UPDATE 3ok_copy1 SET province = " + mongodbData[
            #                             "sheng"] + " WHERE website = '" + data[2] + "';"
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(sql_update)
            #                         # 提交修改
            #                         conn.commit()
            #                         lock.release()
            #                     else:  # 没省
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(
            #                             "UPDATE 3ok_copy1 SET province = '本网站未显示地址' WHERE website = '" + data[2] + "';")
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #
            #                     if mongodbData["shiPinYin"] in line:  # 有市
            #                         sql_update = "UPDATE 3ok_copy1 SET city = " + mongodbData[
            #                             "shi"] + " WHERE website = '" + data[2] + "';"
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(sql_update)
            #                         # 提交修改
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #                     else:  # 没市
            #                         conn.ping(reconnect=True)
            #                         lock.acquire()
            #                         cur.execute(
            #                             "UPDATE 3ok_copy1 SET city = '本网站未显示地址' WHERE website = '" + data[2] + "';")
            #                         conn.commit()
            #                         lock.release()
            #                         pass
            #             # 关闭文件
            #             fo.close()
            #         except:
            #             print("子网址打不开：", urls)
            #             sql_update = "UPDATE 3ok_copy1 SET province = 'contact-us网址打不开' WHERE website = '" + data[
            #                 2] + "';"
            #             conn.ping(reconnect=True)
            #             lock.acquire()
            #             cur.execute(sql_update)
            #             conn.commit()
            #             lock.release()
            # except:
            #     print("主网站打不开:", urls)
            #     sql_update = "UPDATE 3ok_copy1 SET city = '主网站打不开' WHERE website = '" + data[2] + "';"
            #     conn.ping(reconnect=True)
            #     lock.acquire()
            #     cur.execute(sql_update)
            #     conn.commit()
            #     lock.release()
        # driver.close()

if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))

    # 创建线程
    thread_list = []
    for i in range(0, 10):  # 生成10个进程
        th = myThread(i)
        th.start()
        thread_list.append(th)

    for res in thread_list:
        res.join()

    print("Stop at:", time.asctime(time.localtime(time.time())))
