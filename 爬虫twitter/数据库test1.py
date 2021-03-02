import pymysql

# 很好用
# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='twitterdata', charset='utf8')
except:
    print("连接失败")
# 创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象
'''
chaRuSql = "INSERT INTO twtable1 (name, user_name,date,content) VALUES ('miaojiankang','miao','2021年01月19日', 'testContent')"
try:
    # 执行sql语句
    cur.execute(chaRuSql)
    # 提交到数据库执行
    conn.commit()
except:
    # Rollback in case there is any error
    conn.rollback()
'''
cur.execute('select * from twtable1 where content="sss"')
datas = cur.fetchall()
if len(datas):
    print('ssss')
    pass
else:
    print("mm")
    print(datas)

