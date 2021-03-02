import pymysql

# 很好用
# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='test2', charset='utf8')
except:
    print("连接失败")
# 创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象

aa = []
dic = {}
cur.execute('select * from 2_3ok')
data = cur.fetchall()  # 执行sql语句时获取所有行，一行构成一个元组，再将这些元组装入一个元组返回
for d in data:
    # sheng = str(d[7]).strip()  #省
    a = str(d[8]).strip()
    if (len(a)):
        if a in aa:
            dic[a] = dic[a] + 1
            pass
        else:
            aa.append(a)
            dic[a] = 1
# print(aa)
print(sorted(dic.items(), key=lambda kv: (kv[1], kv[0])))

cur.close()  # 关闭对象
conn.close()  # 关闭连接
