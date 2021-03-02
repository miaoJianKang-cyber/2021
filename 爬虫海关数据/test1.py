# -*- coding: utf-8 -*-
import json

import requests

data1 = {}
data1['company_id'] = '1568198'

with open('w_cookies.txt', 'r') as f:  # ,encoding='utf-8'
    listCookies = json.loads(f.read())
cookie = [item["name"] + "=" + item["value"] for item in listCookies]
# print(cookie)
cookiestr = '; '.join(item for item in cookie)
# print(cookiestr)

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "18",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "__root_domain_v=.52wmb.com; _qddaz=QD.oxnn0z.8hqf3r.kjru3sro; _QUY=wqXCh8KywpbCmMKVwplrwpzCk8KeZ8KbwpJnZnDCk2htaQ==; _DP=2; company_search_tips=1; _QP=1; promote=proname=auto; _qdda=3-1.1; _qddab=3-cx3zj9.klpw0b65; access_token=13609ab52b8b529a; 52BY_TOKEN=8ed9a124-7a31-11eb-a26e-00155d391e0d; _MNG=1; vip_expired_tips=none; _qddamta_2885855166=3-0",
    "DNT": "1",
    "Host": "www.52wmb.com",
    "Origin": "https://www.52wmb.com",
    "Referer": "https://www.52wmb.com/buyer/"+str(data1['company_id']),
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
    "X-Requested-With": "XMLHttpRequest",
}
# url = 'https://www.52wmb.com/buyer/{}'.format(data1['company_id'])
url = 'https://www.52wmb.com/async/contact'
data = {
    'company_id': data1['company_id']
}

html = requests.post(url=url, headers=headers, data=data)

if html.status_code == 200:
    print("ok")
    print(html.text)
