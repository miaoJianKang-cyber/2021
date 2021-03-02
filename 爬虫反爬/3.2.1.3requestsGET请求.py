# coding:utf-8
import requests
import re

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50"
# }
#
# response = requests.get("https://www.zhihu.com/explore", headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, response.text)
# print(titles)

datas = "kjygjkhgjhgjh"
url = 'http://www.oupeng.com/sms/sendsms.php?os=s60&mobile=%13673510738'
i_headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
             "Accept": "text/plain", 'Referer': 'http://www.oupeng.com/download'}
# payload=urllib.urlencode(payload)
aa = requests.get(url, headers=i_headers)
print(aa.status_code)

