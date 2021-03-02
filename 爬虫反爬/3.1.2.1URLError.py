# -*- coding: UTF-8 -*-
from urllib import request,error

try:
    response = request.urlopen('http://cuiqingcai.com/index.html')
except error.URLError as e:
    print(e.reason)