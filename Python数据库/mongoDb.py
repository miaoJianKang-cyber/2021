# Python-mongodb教程：https://www.runoob.com/python3/python-mongodb.html

import pymongo

# 链接数据库
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建库名
mydb = myclient["TaobaoDatas"]

# 创建表名
mycol = mydb["CdianpuData"]

# mylist = [
#     {"_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
#     {"_id": 2, "name": "Google", "address": "Google 搜索"},
#     {"_id": 3, "name": "Facebook", "address": "脸书"},
#     {"_id": 4, "name": "Taobao", "address": "淘宝"},
#     {"_id": 5, "name": "Zhihu", "address": "知乎"}
# ]

# 插入数据
# x = mycol.insert_many(mylist)


'''
# 查找集合中一条数据
x = mycol.find_one()
print(x)
'''

# 查找集合中所有数据

# for i in range(0,3):
#     data = mycol.find()
#     for x in data:
#         print(x)
#     for x in data:
#         print(x)
#     for x in data:
#         print(x)
'''
# 查找集合中指定字段的数据
for x in mycol.find({}, {"_id": 0, "name": 1, "alexa": 1}):
    print(x)
'''


# 根据指定条件查询
my_query = {"product_url": "https://be1380715477tgqn.trustpass.alibaba.com/product/1700002232196-820711647/Refined_Sunflower_Oil_At_Affordable_Price_.html"}
my_doc = mycol.find(my_query)
for x in my_doc:
    print(x)


'''
# 修改数据库文档,只修改一条
my_query = {"alexa": "10000"}
new_values = {"$set": {"alexa": "12345"}}
mycol.update_one(my_query, new_values)
# 输出修改后的  "sites"  集合
for x in mycol.find():
    print(x)
'''

'''
# 查找所有以F开头的 name 字段，并将匹配到所有记录的 alexa 字段修改为 123：
my_query = {"name": {"$regex": "^F"}}
new_values = {"$set": {"alexa": "12345678910"}}

x = mycol.update_many(my_query, new_values)
print(x.modified_count, "文档已修改")
for x in mycol.find():
    print(x)
'''

'''
# 排序：sort()
my_doc = mycol.find().sort("alexa")
for x in my_doc:
    print(x)
# '''

'''
# 排序，降序
my_doc = mycol.find().sort("alexa",-1)
for x in my_doc:
    print(x)
'''

'''
# 删除一个文档
my_query = {"name": "Taobao"}
mycol.delete_one(my_query)
# 删除后输出
for x in mycol.find():
    print(x)
'''

'''
# 删除多个文档：删除所有 name 字段中以 F 开头的文档
my_query = {"name": {"$regex": "^F"}}
x = mycol.delete_many(my_query)
print(x.deleted_count, "个文档已删除")
'''

# '''
# 删除所有文档
# x = mycol.delete_many({})
# print(x.deleted_count, "个文档已删除")
# '''

# '''
# 删除集合
# mycol.drop()
# '''

'''
'''
'''
'''
