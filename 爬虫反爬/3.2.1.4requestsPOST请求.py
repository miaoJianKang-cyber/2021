# coding:utf-8
import requests
import re

data = {
    'name': 'germey',
    'age': '22'
}

response = requests.post("http://httpbin.org/post", data=data)
print(response.text)
