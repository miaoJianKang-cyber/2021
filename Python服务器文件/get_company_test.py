#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : keyword                         #
#                                                                   #
#                   @File Name    : get_company1.py                 #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2020/8/10 0010 16:28            #
#                                                                   #
#                   @Last Update  : 2020/8/10 0010 16:28            #
#                                                                   #
#-------------------------------------------------------------------#
# Classes: Use selenium to open a web page to access companies      #
#          with contact information                                 #
#-------------------------------------------------------------------#
'''
from __future__ import absolute_import
from __future__ import with_statement
from queue import Queue
import sys
import re
import json
from lxml import etree
import collections
import requests
import random
import time
import datetime
import io
import pymysql
import codecs
import threading
from PIL import Image
from hashlib import md5
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchFrameException,
    NoSuchWindowException,
    NoSuchElementException,
)

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
# chrome_driver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
information_list = []
# 储存公司信息的列表 /www/wwwroot/www.waiqidian.cn/api/customs/adjunct.json
with open('/www/wwwroot/www.waiqidian.cn/api/customs/comany.txt') as f:
    txt = f.readlines()


# for item in txt:
#     item = item.rstrip("\n")
#     with open('adjunct.json') as f:
#         con_dict = json.loads(f.read())
#     # cookie_path = con_dict['cookie_filepath']
#     cookie_path = 'w_cookies.txt'
#     mysql_db = con_dict[item]['datebase']
#     data_hs = con_dict[item]['hs']
#     try:
#         data_hs = data_hs.split(',')
#     except Exception as e:
#         print('无需分割' + e)


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def readCookies(cookie_path):
    """
    读取本地的cookie并进行遍历
    :param cookie_path:
    :return:
    """
    with open(cookie_path, 'r') as f:  # ,encoding='utf-8'
        listCookies = json.loads(f.read())
    cookie = [item["name"] + "=" + item["value"] for item in listCookies]
    cookiestr = '; '.join(item for item in cookie)
    return cookiestr


def getHTMLText(data, cookiestr):
    """
    # requests请求获取到页面的html
    # :param data:
    # :param cookiestr:
    # :return:
    """
    pageNum = 1
    while pageNum < 5:

        url2 = 'https://www.52wmb.com/async/company?key={}&old_key={}&country=&country_id=0&type=0&sort' \
               '=default&click_search=0&st=3&old_st=3&main=0&extend_search=false&fw%5B%5D=email&filterweight=email&_' \
               '=1604476115171&page={}'.format(data['key'], data['key'], pageNum)
        url1 = 'https://www.52wmb.com/async/company?key={}&old_key={' \
               '}&country=&country_id=0&type=0&sort=default&click_search=0&st=2&old_st=2&main=0&extend_search=false' \
               '&fw%5B%5D=email&filterweight=email&_=1603852119428&page={} '.format(data['key'], data['key'], pageNum)
        url = 'https://www.52wmb.com/async/company?key={}&old_key={' \
              '}&country=&country_id=0&type=0&sort=default&click_search=0&st=3&old_st=3&main=0&extend_search=false&fw' \
              '%5B%5D=email&filterweight=email&_=1603434620022&page={}'.format(data['key'], data['key'], pageNum)
        url3 = 'https://www.52wmb.com/async/company?country=*&key={}&type=0&click_search=1&fw%5B%5D=email&filterweight=email' \
               '&sort=default&country_data=&search_type=3&is_label=1&st=3&page={}&_=1614564485810'.format(data['key'], pageNum)

        headers = {
            'cookie': cookiestr,
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            'referer': 'https://www.52wmb.com/buy-3926909090?st=3'
        }

        try:
            # html = requests.get(url=url2, headers=headers) #miao zhu shi 2021/3/1
            html = requests.get(url=url3, headers=headers)  # miao xin zeng 2021/3/1
            time.sleep(random.randint(4, 8))
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            # print(html.url)
            html = html.text
            information(html, cookiestr)
        except Exception as e:
            print(e)

        pageNum += 1


def information(html, cookiestr):
    """
    # 获取公司的信息
    # :param html:
    # :return:
    """
    companys_list = etree.HTML(html).xpath('//li[@class="ssList-li company-fun-li"]')
    for i in companys_list[:]:
        company_info = collections.OrderedDict()
        try:
            # number 公司id
            c_id = i.xpath('@data-id')[0]
            company_info['number'] = c_id
            # 公司名称
            company_info['name'] = i.xpath('div[1]/div[@class="ssContent"]/a/text()')[0]
            # 地区
            # company_info['trade_country'] = i.xpath('div[1]/div[@class="ssContent"]/p[@class="ss-Ctag"]/text()')[0]
            # 货运次数
            company_info['trade_number'] = i.xpath('div[1]/div[@class="ssContent"]/p[@class="ss-Ctag"]/text()')[1].replace(
                '总货运', '')
            # 更新时间
            update_time = i.xpath('div[1]/div[@class="ssContent"]/div[@class="ss-Cjl"]/text()')[0].strip()[-10:]
            company_info['update_time'] = update_time
            # print("company_info------",company_info)
            get_next_level(company_info, cookiestr)
        except Exception as e:
            print(e)


def get_next_level(company_info, cookiestr):
    url = 'https://www.52wmb.com/async/contact'
    # url = 'https://www.52wmb.com/buyer/35274878?SRID=Z8KWwphnwpZsag%3D%3D&key=crane&st=2'
    data1 = collections.OrderedDict()
    data1['company_id'] = company_info['number']
    # headers = {
    #     'Referer': 'https://www.52wmb.com/buyer/{}'.format(data1['company_id']),
    #     'cookie': cookiestr,
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'

    # } miao zhu shi 2021/3/1
    headers = {
        "Accept": "*/*",
        # "Accept-Encoding": "gzip,deflate,br",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Connection": "keep-alive",
        # "Content-Length": "18",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "__root_domain_v=.52wmb.com; _qddaz=QD.oxnn0z.8hqf3r.kjru3sro; _QUY=wqXCh8KywpbCmMKVwplrwpzCk8KeZ8KbwpJnZnDCk2htaQ==; _DP=2; company_search_tips=1; _QP=1; promote=proname=auto; _qdda=3-1.1; _qddab=3-cx3zj9.klpw0b65; access_token=13609ab52b8b529a; 52BY_TOKEN=8ed9a124-7a31-11eb-a26e-00155d391e0d; _MNG=1; vip_expired_tips=none; _qddamta_2885855166=3-0",
        "DNT": "1",
        "Host": "www.52wmb.com",
        "Origin": "https://www.52wmb.com",
        "Referer": "https://www.52wmb.com/buyer/" + str(data1['company_id']),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
        # "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        'company_id': data1['company_id']
    }

    try:
        html = requests.post(url=url, data=data, headers=headers)  # data=data,
        time.sleep(random.randint(3, 5))
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        # print(html.url)
        html = html.text
        # print('8'*20,'\n',html)
        parser_email(html, company_info)
    except Exception as e:
        return ''


def parser_email(html, company_info):
    html = etree.HTML(html)
    try:

        tbod = html.xpath('//*[@id="contact-detail"]')
        # print("tbod:ss",tbod)
        # titlle = html.xpath('//*[@id="companies-detail"]/div/div/div/h1/text()')//*[@id="contact-detail"]/table/tbody
        if len(tbod) >= 1:
            pass
        else:
            automation()
    except Exception as e:
        pass
    try:
        html = html.xpath('//tbody')[0]
        if len(html) >= 1:
            print('有数据')
        strt = int(time.time())
        company_info['time'] = strt
        company_info['tableid'] = 0
        company_info['spider'] = 1
        try:
            # 数据来源
            region = html.xpath('tr[4]/td[1]/text()')[1].strip()
        except:
            region = '-'
        company_info['region'] = region
        try:
            # 联系电话
            c_tel = html.xpath('tr[3]/td[1]/text()')[1].strip()
        except:
            c_tel = '-'
        company_info['tel'] = c_tel

        try:
            # 联  系  人
            lianxiren = html.xpath('tr[2]/td[1]/text()')[1].strip()
        except:
            lianxiren = '-'
        company_info['lianxiren'] = lianxiren
        try:
            # 邮箱地址
            c_email = html.xpath('tr[2]/td[2]/text()')[1].strip()
        except:
            c_email = '-'
        company_info['company_email'] = c_email
        try:
            # 公司地址
            c_adress = html.xpath('tr[3]/td[2]/text()')[1].strip()
        except:
            c_adress = '-'
        company_info['company_address'] = c_adress
        # try:
        #     # 数据来源
        #     c_source = html.xpath('tr[4]/td[1]/text()')[1].strip()
        # except:
        #     c_source = '-'
        # company_info['company_source'] = c_source
        try:
            # 官方网站
            c_site = html.xpath('tr[4]/td[2]/a/text()')[0]
        except:
            c_site = '-'
        company_info['company_site'] = c_site
    except Exception as e:
        print('没有数据' + e)
    if len(company_info) > 10:
        information_list.append(company_info)
        print(json.dumps(company_info, ensure_ascii=False))
    else:
        print('数据不完整')


def Verification(companys_list):
    """
    # 判断页面是否请求成功是否拿到信息
    # :param companys_list:
    # :return:
    """
    all_dict = collections.OrderedDict()
    if len(companys_list) > 0:
        all_dict['code'] = 200
        all_dict['msg'] = "sucess"
    else:
        all_dict['code'] = 404
        all_dict['msg'] = "没有找到该信息，请更换关键词再试试"
    test_dict = collections.OrderedDict()
    test_dict['number'] = '1111111'
    test_dict['name'] = 'name'
    test_dict['update_time'] = time.strftime('%Y-%m-%d')
    test_dict['other_trade'] = 'None'
    # companys_list[-1] = test_dict
    all_dict['data'] = companys_list
    print(json.dumps(companys_list, ensure_ascii=False))
    insert_company(companys_list)
    # 插入数据库
    if all_dict['code'] == 404:
        Verification_code()


def insert_company(mysql_db):
    """
    # 把信息插入数据库
    # :param data:
    # :return:
    """
    strt = int(time.time())
    try:
        conn = pymysql.connect(host=mysql_db['host'],
                               user=mysql_db['user'],
                               password=mysql_db['password'],
                               database=mysql_db['user'],
                               charset='utf8')
        cursor = conn.cursor()
        print("数据库连接成功")
    except Exception as e:
        print(e)
        return
    if len(information_list) >= 0:
        # print("准备插入数据库->",information_list)
        # print("数据库信息->",mysql_db['host'],mysql_db['user'],mysql_db['password'],mysql_db['user'])

        list1 = [tuple([i["update_time"]] +
                       [i['name']] +
                       [i["trade_number"]] +
                       [i["region"]] +
                       [i["company_email"]] +
                       [i["lianxiren"]] +
                       [i["tel"]] +
                       [i['company_address']] +
                       [i["company_site"]] +
                       [i["time"]] +
                       [i["tableid"]] +
                       [i["spider"]]
                       ) for i in information_list]

        for data in list1:
            insert_sql = 'insert into wp_haiguan_data (day,company_name,number,country,email,lianxiren,phone,address,' \
                         'website,update_time,tableid,is_spider) values {};'.format(data)
            try:
                # print("插入数据库的sql语句",insert_sql)
                cursor.execute(insert_sql)
                conn.commit()
            except Exception as e:
                print(e)
        cursor.close()
        conn.close()
    else:
        print('没有数据')


def automation():
    """
    解决验证码,验证码处出来截图并连接打码平台
    :return:
    """

    driver = webdriver.Chrome(options=chrome_options)
    """
    处理selenium被检测这个问题
    """
    driver.maximize_window()
    driver.get('https://www.52wmb.com/buyer/35206685?SRID=acKVwpdnwpdrbA%3D%3D&key=mask&st=2')
    with open('w_cookies.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies
    for cookie in listCookies:
        cookie_dict = {

            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        # 添加cookie进行免登陆
        driver.add_cookie(cookie_dict)
    # 刷新当前页面
    driver.refresh()
    time.sleep(2)
    # 切换iframe
    driver.switch_to.frame('mainFrame')
    # 定位验证码图片位置
    xi = driver.find_element_by_xpath('//*[@id="picture"]')
    # 截取整个页面,为下面截取验证码用
    driver.save_screenshot('page.png')
    # 根据验证码定位元素来获取长宽高
    left = xi.location['x']
    top = xi.location['y']
    right = xi.location['x'] + xi.size['width']
    bottom = xi.location['y'] + xi.size['height']
    # 打开整个页面截图
    im = Image.open('page.png')
    # 截取验证码图片
    im = im.crop((left, top, right, bottom))
    # 保存到本地
    im.save('pages.png')
    time.sleep(3)
    # 连接打码平台
    cjy = Chaojiying_Client
    chaojiying = Chaojiying_Client('20200807', 'ht123456789',
                                   '907025')  # 用户中心>>软件ID 生成一个替换 96001
    img = open('pages.png', 'rb').read()  # 本地图片文件路径 来替后要加()换 a.jpg 有时WIN系统
    msg = chaojiying.PostPic(img, 1902)
    yzm = msg['pic_str']
    # 输入平台传回来的验证码并输入
    driver.find_element_by_id('picture_code').send_keys(yzm)
    time.sleep(1)
    driver.find_element_by_id('verifi_robot').click()
    time.sleep(3)
    # 退出当前iframe表单
    driver.switch_to.default_content()
    driver.refresh()
    driver.quit()


def Verification_code():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.52wmb.com/buy-mask?st=2')
    driver.maximize_window()
    with open(r'w_cookies.txt', 'r+') as f:
        list_cookies = json.loads(f.read())
    for item in list_cookies:
        cookie_dict = {
            'name': item.get('name'),
            'value': item.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict=cookie_dict)
    driver.refresh()
    # 清空跳转框数值
    driver.find_element_by_xpath('//*[@id="company_list_input"]').clear()
    # 填入随机页数
    driver.find_element_by_xpath('//*[@id="company_list_input"]').send_keys(random.randint(5, 9))
    # 点击跳转
    driver.find_element_by_xpath('//*[@id="company_list_jump"]').click()
    time.sleep(2)
    try:
        driver.switch_to.frame('mainFrame')
        # 定位验证码图片位置
        xi = driver.find_element_by_xpath('//*[@id="picture"]')
        # 截取整个页面,为下面截取验证码用
        driver.save_screenshot('page.png')
        # 根据验证码定位元素来获取长宽高
        left = xi.location['x']
        top = xi.location['y']
        right = xi.location['x'] + xi.size['width']
        bottom = xi.location['y'] + xi.size['height']
        # 打开整个页面截图
        im = Image.open('page.png')
        # 截取验证码图片
        im = im.crop((left, top, right, bottom))
        # 保存到本地
        im.save('pages.png')
        time.sleep(1)
        # 连接打码平台
        cjy = Chaojiying_Client
        chaojiying = Chaojiying_Client('20200807', 'ht123456789',
                                       '907025')  # 用户中心>>软件ID 生成一个替换 96001
        img = open('pages.png', 'rb').read()  # 本地图片文件路径 来替后要加()换 a.jpg 有时WIN系统
        msg = chaojiying.PostPic(img, 1902)
        yzm = msg['pic_str']
        # 输入平台传回来的验证码并输入
        driver.find_element_by_id('picture_code').send_keys(yzm)
        time.sleep(1)
        driver.find_element_by_id('verifi_robot').click()
        time.sleep(1)
        # 退出当前iframe表单
        driver.switch_to.default_content()
    except Exception as e:
        print(e)
    driver.quit()


if __name__ == '__main__':
    start = time.time()
    for item in txt:
        item = item.rstrip("\n")
        # print(item,'ee')
        with open('/www/wwwroot/www.waiqidian.cn/api/customs/adjunct.json') as f:
            con_dict = json.loads(f.read())
        cookie_path = con_dict['cookie_filepath']
        # # cookie_path = 'w_cookies.txt'
        mysql_db = con_dict[item]['datebase']
        data_hs = con_dict[item]['hs']
        try:
            data_hs = data_hs.split(',')
        except Exception as e:
            print('无需分割' + e)
        # print(data_hs)

        for hs in data_hs:
            data1 = collections.OrderedDict()
            data1['key'] = hs
            cookie = readCookies(cookie_path)
            getHTMLText(data1, cookie)
            insert_company(mysql_db)
            list1 = [tuple([i["update_time"]] +
                           [i['name']] +
                           [i["trade_number"]] +
                           [i["region"]] +
                           [i["lianxiren"]] +
                           [i["tel"]] +
                           [i["company_address"]] +
                           [i['company_email']] +
                           [i["company_site"]] +
                           [i["time"]] +
                           [i["tableid"]] +
                           [i["spider"]]
                           ) for i in information_list]
            print("List1aaa:", list1)

    print('时间', time.time() - start)

'''
{"day": '日期', "company_name": '公司名称', "number" :'货运次数', "email": '邮箱', "lianxiren": '联系人', "fax" :'电话', "address": '地址',
 "website": '网址', "update_time": '添加时间'}
'''
