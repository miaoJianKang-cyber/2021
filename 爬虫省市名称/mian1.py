# -*- coding: utf-8 -*-  
# 链接数据库
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["DATA(province_city_cant_delete)"]

# 创建表名
mycol = mydb["province_city"]


def main():
    flag = 1
    province = ""
    with open('C:/Users/18003/Desktop/new 1.txt', 'r', encoding='utf-8') as f:
        for each_line in f:
            print(each_line)
            if flag == 1:
                # 省
                province = each_line
                flag = 2
            else:
                flag = 1
                data = [
                    {"sheng": province,
                     "shi": each_line},
                ]
                mycol.insert_many(data)

    pass


if __name__ == "__main__":
    print("Start...")
    main()
    pass
