# -*- coding: UTF-8 -*-
import os
import subprocess

# pymongo
import time

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol3ok_copy = mydb["3ok_copy1"]

my_query = {"website": "cpa-pipesupports.com"}
new_values = {"$set": {"website_ok": "False"}}
x = mycol3ok_copy.update_many(my_query, new_values)
print(x.modified_count, "文档已修改")

mongodb3ok_copyDatas = mycol3ok_copy.find()
for mongodb3ok_copyData in mongodb3ok_copyDatas:
    # print(mongodb3ok_copyData)
    # print(mongodb3ok_copyData["website_ok"])
    # print(type(mongodb3ok_copyData))
    # if mongodb3ok_copyData["website_ok"] == "":
    #     print(mongodb3ok_copyData)
    if "website_ok" not in mongodb3ok_copyData:
        # print("不存在")
        print(mongodb3ok_copyData["website"])
        # time.sleep(3)


        ip = mongodb3ok_copyData["website"]
        result = os.system('ping -n 1 -w 1 {}'.format(ip))
        if result:  # 根的失败
            if "www" not in ip:
                ipwww = "www." + ip
                result = os.system('ping -n 1 -w 1 {}'.format(ipwww))
                if result:
                    # 加http
                    iphttp = "http://" + ipwww
                    result = os.system('ping -n 1 -w 1 {}'.format(iphttp))
                    if result:  # 支失败
                        iphttps = "https://" + ipwww
                        result = os.system('ping -n 1 -w 1 {}'.format(iphttps))
                        if result:
                            my_query = {"website": mongodb3ok_copyData["website"]}
                            new_values = {"$set": {"website_ok": "False"}}
                            mycol3ok_copy.update_many(my_query, new_values)
                        else:
                            my_query = {"website": mongodb3ok_copyData["website"]}
                            new_values = {"$set": {"website_ok": "True"}}
                            mycol3ok_copy.update_many(my_query, new_values)
                            print(mongodb3ok_copyData["website"],"True")

                    else:
                        my_query = {"website": mongodb3ok_copyData["website"]}
                        new_values = {"$set": {"website_ok": "True"}}
                        mycol3ok_copy.update_many(my_query, new_values)
                        print(mongodb3ok_copyData["website"], "True")
                else:
                    my_query = {"website": mongodb3ok_copyData["website"]}
                    new_values = {"$set": {"website_ok": "True"}}
                    mycol3ok_copy.update_many(my_query, new_values)
                    print(mongodb3ok_copyData["website"], "True")
            else:
                # 加http
                iphttp = "http://" + ip
                result = os.system('ping -n 1 -w 1 {}'.format(iphttp))
                if result:  # 支失败
                    iphttps = "https://" + ip
                    result = os.system('ping -n 1 -w 1 {}'.format(iphttps))
                    if result:
                        my_query = {"website": mongodb3ok_copyData["website"]}
                        new_values = {"$set": {"website_ok": "False"}}
                        mycol3ok_copy.update_many(my_query, new_values)
                    else:
                        my_query = {"website": mongodb3ok_copyData["website"]}
                        new_values = {"$set": {"website_ok": "True"}}
                        mycol3ok_copy.update_many(my_query, new_values)
                        print(mongodb3ok_copyData["website"], "True")
                else:
                    my_query = {"website": mongodb3ok_copyData["website"]}
                    new_values = {"$set": {"website_ok": "True"}}
                    mycol3ok_copy.update_many(my_query, new_values)
                    print(mongodb3ok_copyData["website"], "True")
        else:
            my_query = {"website": mongodb3ok_copyData["website"]}
            new_values = {"$set": {"website_ok": "True"}}
            mycol3ok_copy.update_many(my_query, new_values)
            print(mongodb3ok_copyData["website"], "True")

