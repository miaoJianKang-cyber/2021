# coding:utf-8
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as  pq
import json

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print('Error', e.args)


def parse_page(json1):
    if json1:
        json1 = json.loads(json1)
        items = json1.get('data')
        items = items.get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get("text")).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comment'] = item.get('comment_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo


if __name__ == "__main__":
    for page in range(1, 11):
        json1 = get_page(page)
        results = parse_page(json1)
        for result in results:
            print(result)
