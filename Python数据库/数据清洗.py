import pymysql
# 很好用
# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost',user='root',port=3306,passwd='123456',db='test2',charset='utf8')
except:
    print("连接失败")
#创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象

cur.execute('select * from 3hou21ye')
lines = cur.fetchall() #执行sql语句时获取所有行，一行构成一个元组，再将这些元组装入一个元组返回
for line in lines:
    print(line[3])
    if 'E' in line[3]:
        del_sql_line = "delete from 3hou21ye where telephone='{}';".format(line[3])
        # 执行SQL语句
        cur.execute(del_sql_line)
        # 提交修改
        conn.commit()
        print("删除成功")


cur.close()#关闭对象
conn.close()#关闭连接