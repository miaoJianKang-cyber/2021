# -*- coding: utf-8 -*-  
# 链接数据库
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol = mydb["province_city"]



data = [
{"sheng": "香港特别行政区"},
{"sheng": "澳门特别行政区"},

]
mycol.insert_many(data)


if __name__ == "__main__":
    print("Start...")
    pass
