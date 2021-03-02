# -*- coding: UTF-8 -*-

# 成功
# 功能：将图片导入到MySQL数据库

import pymysql




# 读取图片文件
fp = open("C:/Users/18003/Pictures/Camera Roll/2.jpg", 'rb')
img = fp.read()
fp.close()

# 建立一个MySQL连接
conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='test2', charset='utf8')

# 创建游标
cursor = conn.cursor()

sql = "INSERT INTO vbp_person_ext VALUES  (%s, %s, %s);"
args = ('41',  img,'112')
cursor.execute(sql, args)
# 提交到数据库
conn.commit()




# 关闭游标
cursor.close()
# 关闭数据库连接
conn.close()

print("Done! ")
