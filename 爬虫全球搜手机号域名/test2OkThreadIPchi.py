# -*- coding: UTF-8 -*-
import csv
import threading
import requests  # 替代浏览器发送网络请求
import json  # json --字典 方便数据获取
import time



lock = threading.Lock()
ip_list = []
def get_ip_list():
    global ip_list
    if len(ip_list) == 0:
        try:
            ip_api_url = "http://api.wandoudl.com/api/ip?app_key=e944c8cbf42c3c941dc7f15bc905e394&pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&area_id=410700 "
            resp = requests.get(ip_api_url)
            # 提取页面数据
            resp_json = resp.text
            # json字符串 -- 字典
            resp_dict = json.loads(resp_json)
            ip_list = resp_dict.get('data')
        except:
            print("今日豌豆荚ip代理池数量已经使用完。")
    ip_list_copy = ip_list[0]
    ip_list.remove(ip_list[0])
    return ip_list_copy


class myThread(threading.Thread):
    def __init__(self, threadID, start_num, end_num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.start_numA = start_num
        self.end_numA = end_num


    def run(self):
        # print("开始线程:"+str(self.threadID),end='\n')
        print(self.start_numA,"---",self.end_numA,end='\n')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'}
        # 代理ip地址放在Proxy参数当中
        # 获取代理IP池
        lock.acquire()
        ip_dict = get_ip_list()
        lock.release()
        ip_port = '{ip}:{port}'.format(ip=ip_dict.get('ip'),port=str(ip_dict.get('port')))
        proxies = {"http": 'http://{}'.format(ip_port)}
        for i in range(self.start_numA, self.end_numA+1):
            j = str(i).zfill(5)  # -------------------------------------------------------------------------------------添加到ip的剩余几位数，必须改
            url = "https://www.quanqiusou.cn/design/186374" + str(j) + "/" # -------------------------------------------访问域名，位数需要与上面的对着，必须改
            try:
                r = requests.get(url,proxies=proxies,headers=headers,timeout=1)
                if r.status_code == 200:
                    print(url)
                    try:
                        with open('url.csv', 'a', newline="",
                                  encoding='utf-8') as filecsv:  # -----------------------------------------------------保存的文件名
                            caswriter = csv.writer(filecsv)
                            caswriter.writerow(url)
                    except:
                        print("保存数据错误一次")
            except requests.exceptions.Timeout:
                lock.acquire()
                ip_dict = get_ip_list()
                lock.release()
                ip_port = '{ip}:{port}'.format(ip=ip_dict.get('ip'),port=str(ip_dict.get('port')))
                proxies = {"http": 'http://{}'.format(ip_port)}


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))

    # 创建线程
    thread_list = []
    for i in range(0,10):# 生成10个进程
        th = myThread(i,i*10000,i*10000+9999) #  -----------------------------------------------------------------------添加到访问域名的剩余几位数，五位数就乘10000，四位数就乘1000
        th.start()
        thread_list.append(th)

    for res in thread_list:

        res.join()

    print("Stop at:", time.asctime(time.localtime(time.time())))

