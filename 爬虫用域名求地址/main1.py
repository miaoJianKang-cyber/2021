# -*- coding: utf-8 -*-  
# 用company_name中含有的地址信息计算
import time

import pymongo

# pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol3ok_copy = mydb["3ok_copy1"]
mycolprovince_city_PinYin = mydb["province_city_PinYin"]


def main():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        FlagA = 1
        mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find()
        company_name = mycol3ok_copyData["company_name"].lower()
        if mycol3ok_copyData["province"] is not None:  # 省份不是空
            if "省" not in mycol3ok_copyData["province"]:  # 不含"省"字
                for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                    if mycolprovince_city_PinYinData["shiPinYin"] in company_name:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                        mycol3ok_copy.update_one(my_query, new_values)
                        FlagA = 2
                    if mycolprovince_city_PinYinData["shengPinYin"] in company_name:
                        my_query = {"_id": mycol3ok_copyData["_id"]}
                        new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                        mycol3ok_copy.update_one(my_query, new_values)
                        FlagA = 2
                    if FlagA == 2:
                        continue

        else:  # 省份是空
            for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                if mycolprovince_city_PinYinData["shengPinYin"] in company_name:
                    my_query = {"_id": mycol3ok_copyData["_id"]}
                    new_values = {"$set": {"province": mycolprovince_city_PinYinData["sheng"]}}
                    mycol3ok_copy.update_one(my_query, new_values)
                    FlagA = 2

                if mycolprovince_city_PinYinData["shiPinYin"] in company_name:
                    my_query = {"_id": mycol3ok_copyData["_id"]}
                    new_values = {"$set": {"city": mycolprovince_city_PinYinData["shi"]}}
                    mycol3ok_copy.update_one(my_query, new_values)
                    FlagA = 2
                if FlagA == 2:
                    continue


if __name__ == "__main__":
    print("Start...")
    main()
    pass
