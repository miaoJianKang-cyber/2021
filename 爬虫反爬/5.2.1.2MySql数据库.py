# coding:utf-8
import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='test2', charset='utf8')
except:
    print("连接失败")
# 创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象
cur.execute('SELECT VERSION()')
data = cur.fetchone()
print(data)