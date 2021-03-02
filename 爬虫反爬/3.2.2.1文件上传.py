# coding:utf-8
import requests


files = {'file':open('cookies.txt','rb')}
r = requests.post("http://httpbin.org/post",files=files)
print(r.text)