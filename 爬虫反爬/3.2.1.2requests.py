# coding:utf-8
import requests
for item in range(1,5):
    print(item)
response = requests.get("http://www.baidu.com")
# print(type(response))
print(response.status_code)
# print(type(response.text))
# print(response.text)
# print(response.cookies)

# r = requests.post('http://httpbin.org/post')
# r = requests.put('http://httpbin.org/post')
# r = requests.delete('http://httpbin.org/post')
# r = requests.head('http://httpbin.org/post')
# r = requests.options('http://httpbin.org/post')
def miao():
    print("ssss")

miao()

if __name__ == '__main__':
    miao()