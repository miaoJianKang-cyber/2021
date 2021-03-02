# -*- coding: utf-8 -*-  
# url:http://w120.waiqidian.cn/sitemap.xml
# author:miaoJianKang
import requests
from bs4 import BeautifulSoup

url = "http://w120.waiqidian.cn/sitemap.xml"

def main():
    num = 1
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html,features="lxml")
        urls_NoY = soup.find_all('loc')
        for url_NoY in urls_NoY:
            url_NoY = url_NoY.string
            response_NoY = requests.get(url_NoY)
            if response_NoY.status_code == 200:
                html_NoE = response_NoY.text
                soup_NoE = BeautifulSoup(html_NoE,features="lxml")
                urls_NoE = soup_NoE.find_all('loc')
                for url_NoE in urls_NoE:
                    url_NoE = url_NoE.string
                    response_NoY = requests.get(url_NoE)
                    if response_NoY.status_code == 200:
                        num += 1

    else:
        print("*"*50,"url--->Error,please check.","*"*50,sep='\n')
    print(num, "num")

if __name__ == "__main__":
    print("Start...")
    main()
    pass
