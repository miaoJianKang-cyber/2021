import time  # 引入time模块
from selenium import webdriver
import csv

def search_product(keyword):
    driver.find_element_by_id('q').send_keys(keyword)
    driver.find_element_by_class_name('btn-search').click()
    driver.maximize_window()
    driver.implicitly_wait(10)  # 浏览器等待
    pass

def get_product():
    divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        info=div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text  #商品名称
        price=div.find_element_by_xpath('.//strong').text+'元' #商品价格
        deal=div.find_element_by_xpath('.//div[@class="deal-cnt"]').text  #付款人数
        name=div.find_element_by_xpath('.//div[@class="shop"]/a').text  #店铺名称
        print(info,price,deal,name,sep='|')
        with open('data.csv','a',newline="") as filecsv:
            caswriter = csv.writer(filecsv,delimiter=",")
            caswriter.writerow([info,price,deal,name])
    pass

def main():
    search_product(keyword)
    get_product()

if __name__ == '__main__':
    print("Run Ok at->",time.asctime(time.localtime(time.time())))

    # 开始
    # keyword = input("请输入你要搜索的商品关键字： ")
    keyword = "裤子"
    driver = webdriver.Chrome()
    driver.get('https://www.taobao.com/')
    main()































