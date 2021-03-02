# -*- coding: UTF-8 -*-
from urllib import  request,parse

url = "http://httpbin.org/post"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
}
dict = {"name":"Germey"}

data = bytes(parse.urlencode(dict),encoding="utf-8")
req = request.Request(url=url,data=data,headers=headers,method="POST")
response = request.urlopen(req)
print(response.read().decode('utf-8'))