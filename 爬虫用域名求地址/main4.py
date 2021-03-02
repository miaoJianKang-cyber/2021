# -*- coding: utf-8 -*-  
# 用含有城市的值赋予省份的值

# pymongo
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol3ok_copy = mydb["3ok_copy1_02.20"]
mycolprovince_city_PinYin = mydb["province_city_PinYin"]


def main():
    mycol3ok_copyDatas = mycol3ok_copy.find()
    for mycol3ok_copyData in mycol3ok_copyDatas:
        province = mycol3ok_copyData["province"]
        city = mycol3ok_copyData["city"]
        if city is not None:

            mycolprovince_city_PinYinDatas = mycolprovince_city_PinYin.find({"shi":city})
            for mycolprovince_city_PinYinData in mycolprovince_city_PinYinDatas:
                if  mycolprovince_city_PinYinData["sheng"] != province:
                    print(province,city,mycolprovince_city_PinYinData["sheng"],sep="---")
                    my_query = {"_id": mycol3ok_copyData["_id"]}
                    new_values = {"$set":
                                      {"province": mycolprovince_city_PinYinData["sheng"],
                                       }
                                  }
                    x = mycol3ok_copy.update_one(my_query, new_values)
                    print(x.matched_count, "受影响")



pass

if __name__ == "__main__":
    print("Start...")
    main()
    pass
