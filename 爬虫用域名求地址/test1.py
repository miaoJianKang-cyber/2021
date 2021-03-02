# -*- coding: UTF-8 -*-
import time

import pymysql
import requests  # 替代浏览器发送网络请求
from bs4 import BeautifulSoup
from selenium import webdriver

# 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(5)
driver.set_script_timeout(5)  # 这两种设置都进行才有效

try:
    conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='test2', charset='utf8')
except:
    print("连接失败")
# 创建一个对象，用于执行sql语句
cur = conn.cursor()  # 创建一个对象

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/537.36',

}

cur.execute('select * from 3ok_copy1')
datas = cur.fetchall()  # 执行sql语句时获取所有行，一行构成一个元组，再将这些元组装入一个元组返回
for data in datas:
    print(data)
    for i in range(0,len(data)):
        print(data[i])
    print(data[7])
    print(data[8])
    print(data[6])
    print(data[5])
    print(data[4])
    print(data[3])
    print(data[2])
    print(data[1])
    if data[7] == None and data[8] == None:
        url = "http://" + str(data[2])
        urls = "https://" + str(data[2])
        try:
            r = requests.get(url, headers=headers)
            rs = requests.get(urls,headers=headers)
            if r.status_code == 200 or rs.status_code == 200:
                try:
                    if r.status_code ==200:
                        url = "http://" + str(data[2]) + "/contact-us"
                        driver.get(url)
                    else:
                        urls = "https://" + str(data[2]) + "/contact-us"
                        driver.get(urls)

                except:
                    print("子网址打不开：",url)
                    sql_update = "UPDATE 3ok_copy1 SET province = 'contact-us网址打不开' WHERE website = '" + data[2] + "';"
                    cur.execute(sql_update)
                    conn.commit()
                    continue
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                elem_data = soup.prettify()
                # print(type(elem_data))
                # 打开一个文件
                fo = open("elements.txt", "w", encoding='utf-8')
                fo.write(elem_data)
                # 关闭打开的文件
                fo.close()

                # 打开文件
                fo = open("elements.txt", "r", encoding="utf-8")
                sql_update = ""
                for line in fo.readlines():  # 依次读取每行
                    line = line.strip()  # 去掉每行头尾空白
                    if "hebei" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '河北省' WHERE website = '" + data[2] + "';"
                    if "shanxi" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '山西省/陕西省' WHERE website = '" + data[2] + "';"
                    if "liaoning" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '辽宁省' WHERE website = '" + data[2] + "';"
                    if "jilin" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '吉林省' WHERE website = '" + data[2] + "';"
                    if "heilongjiang" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '黑龙江省' WHERE website = '" + data[2] + "';"
                    if "jiangsu" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '江苏省' WHERE website = '" + data[2] + "';"
                    if "anhui" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '安徽省' WHERE website = '" + data[2] + "';"
                    if "fujian" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '福建省' WHERE website = '" + data[2] + "';"
                    if "shandong" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '山东省' WHERE website = '" + data[2] + "';"
                    if "henan" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '河南省' WHERE website = '" + data[2] + "';"
                    if "hubei" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '湖北省' WHERE website = '" + data[2] + "';"
                    if "hunan" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '湖南省' WHERE website = '" + data[2] + "';"
                    if "guangdong" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '广东省' WHERE website = '" + data[2] + "';"
                    if "hainan" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '海南省' WHERE website = '" + data[2] + "';"
                    if "guizhou" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '贵州省' WHERE website = '" + data[2] + "';"
                    if "yunnan" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '云南省' WHERE website = '" + data[2] + "';"
                    if "gansu" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '甘肃省' WHERE website = '" + data[2] + "';"
                    if "qinghai" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '青海省' WHERE website = '" + data[2] + "';"
                    if "taiwan" in line.lower():
                        sql_update = "UPDATE 3ok_copy1 SET province = '台湾省' WHERE website = '" + data[2] + "';"
                print(sql_update)
                if len(sql_update) > 2:
                    cur.execute(sql_update)
                    # 提交修改
                    conn.commit()
                # print(line)
                # 关闭文件
                fo.close()

        except:
            print("主网站打不开:", url)
            sql_update = "UPDATE 3ok_copy1 SET city = '主网站打不开' WHERE website = '" + data[2] + "';"
            cur.execute(sql_update)
            conn.commit()
