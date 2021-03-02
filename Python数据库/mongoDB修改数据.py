# -*- coding: utf-8 -*-

# 链接数据库
import pymongo
import pypinyin

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol = mydb["province_city"]
mycolPinYin = mydb["province_city_PinYin"]


def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


def main1():
    # 查找集合中指定字段的数据
    for x in mycolPinYin.find():
        # print(x)
        if "盟" in x["shi"]:
            # print(x)
            myquery = {"shi": x['shi']}
            newvalues = {"$set": {"shiPinYin": pinyin(x['shi'].replace("盟", ""))}}
            mycolPinYin.update_one(myquery, newvalues)
        pass
    pass


if __name__ == "__main__":
    print("Start...")
    main1()
    pass
