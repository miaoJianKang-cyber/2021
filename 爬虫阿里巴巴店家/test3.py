# -*- coding: utf-8 -*-  

# 实例化配置文件
import configparser
import time
import pymongo
from docx import Document

Doc = Document()

Doc.add_heading("Python是什么东西？？？")  # 添加标题

'''
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
for list in db_data_col_Data.find():
    print(config.get('Parameter', "url"))
    print(list["catalogue_name"])
    print(list["product_url"])
    print(list["Overview"])
    print(list["imagesDescription"])
    print(list["keywords"])
    print(list["mainImage"])
    print(list["productDescription"])
    print(list["title"])
    time.sleep(1)
'''
