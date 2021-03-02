# -*- coding: UTF-8 -*-
import requests     # 替代浏览器发送网络请求
import base64       # 加密手段
import json         # json --字典 方便数据获取
import threading    # 多线程
# 从哔哩哔哩上看到的



'''
第1部分：获取代理ip和对应的端口号
'''
def get_ip_list():
    url = 'http://api.wandoudl.com/api/ip?app_key=e944c8cbf42c3c941dc7f15bc905e394&pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&area_id=410700'
    resp = requests.get(url)
    # 提取页面数据
    resp_json = resp.text
    # json字符串 -- 字典
    resp_dict = json.loads(resp_json)

    ip_dict_list = resp_dict.get('data')
    return ip_dict_list

'''
第2部分：访问代理ip服务器需要做的准备
'''
# 验证信息 --用户名+密码  加密编码，放在headers参数里
def base_code(username,password):
    str = '%s:%s' % (username,password)
    encodestr = base64.b64encode(str.encode('utf-8'))
    return '%s' % encodestr.decode()



'''
第3部分：用代理ip对目标网站发送网络请求，并且获取相关数据
'''

def spider_ip(ip_port,url):  # 1:ip_port,2"真正要请求的ip
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
        # 'Proxy-Authorization':authorization
    }
    # 代理ip地址放在Proxy参数当中
    proxies = {
        "http": 'http://{}'.format(ip_port),
    }
    # 发送网络请求
    try:
        resp = requests.get(url,proxies=proxies,headers=headers)
        #解析访问的数据
        result =resp.text
        print(url)
    except:
        result = '此代理失效'
    print('当前线程：',threading.current_thread(),'\n'+result)


if __name__ == '__main__':
    username = '18003962410@189.cn'
    password = 'MIao2493'
    # 加密后的验证信息
    authorization = 'Basic %s' % (base_code(username,password))

    # 要真正访问的网址
    url = 'http://myip.ipip.net/'

    # 获取代理IP池
    ip_dict_list = get_ip_list()

    #多线程发送网络请求
    i = 1
    for ip_dict in ip_dict_list:
        # 获取每次代理ip以及端口
        ip_port = '{ip}:{port}'.format(ip=ip_dict.get('ip'),port=str(ip_dict.get('port')))

        # 创建线程
        ip_threading = threading.Thread(target=spider_ip,args=(ip_port,url))

        # 给每条线程按照创建顺序命名
        ip_threading.name = '线程%d' % i
        ip_threading.start()
        i += 1
        pass










'''
# 以json格式返回数据
url = "http://api.wandoudl.com/api/ip?app_key=e944c8cbf42c3c941dc7f15bc905e394&pack=0&num=20&xy=1&type=2&lb=\r\n&mr=1&area_id=410700"

response = requests.get(url)
print(type(response))
print(response.json())
print(type(response.json()))
'''