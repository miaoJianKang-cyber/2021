# -*- coding: UTF-8 -*-

import pymysql

try:
    conn = pymysql.connect(host='localhost',user='root',port=3306,passwd='123456',db='test2',charset='utf8')
except:
    print("连接失败")
#创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象


cur.execute('select * from 3ok_copy1')
datas = cur.fetchall() #执行sql语句时获取所有行，一行构成一个元组，再将这些元组装入一个元组返回
for data in datas:
    print(data[2])
    if "E" in data[2]:
        sql = "delete from 3ok_copy1 where telephone ='" + data[2] + "';"
        cur.execute(sql)
        conn.commit()
        print("删除成功")

cur.close()#关闭对象
conn.close()#关闭连接