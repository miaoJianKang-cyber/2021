import requests

def login():
    login_url = 'http://www.baidu.com'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    body = {
        "company_id": "liuzz05@****.com",
        "password": "123456"
    }
    try:
        res = requests.post(url=login_url, headers=headers, data=body)
        cookies = res.cookies.items()

        cookie = ''
        for name, value in cookies:
            cookie += '{0}={1};'.format(name, value)

        return cookie
    except Exception as err:
        print('获取cookie失败：\n{0}'.format(err))



get_data_url = 'http://www.baidu.com'

cookie = login()
headers = {
    "cookie": cookie
}
res = requests.get(url=get_data_url, headers=headers)
print(res.text)