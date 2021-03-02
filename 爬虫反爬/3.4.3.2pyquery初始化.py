# coding:utf-8
from pyquery import PyQuery as pq

doc = pq(url="https://cuiqingcai.com")
print(doc('title'))
