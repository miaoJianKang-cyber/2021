# coding:utf-8
import requests
from pyquery import PyQuery

url = "https://www.zhihu.com/expore"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50"
}

html = requests.get(url,headers=headers).text
doc = PyQuery(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = PyQuery(item.find('.content').html()).text()
    file = open('explore.txt','a',encoding='utf-8')
    file.write('\n'.join([question, author, answer]))
    file.write('\n'+'='*50+'\n')
    file.close()