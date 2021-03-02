# url爬取
# 保存到数据库

import io
import sys
import time  # 引入time模块

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码


def openChrome():
    # get直接返回，不再等待界面加载完成
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"

    # 设置selenium自动化Chrome浏览器的图片不加载，2就是不加载
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)

    # 设置无界面模式
    opt = Options()
    opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
    opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
    opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
    opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
    driver = webdriver.Chrome(options=opt)  # 创建无界面对象

    url = "https://twitter.com/search?q=" + keyword + "&src=typed_query"
    driver.get(url)
    return driver


def getData(driver, conn):
    time.sleep(3)
    cur = conn.cursor()  # 数据库创建一个对象
    for i in range(1, 10):
        time.sleep(1)
        driver.maximize_window()
        js = 'window.scrollBy(0,1000)'
        driver.execute_script(js)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find_all('div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
        for div in divs:
            try:
                name = div.find(
                    'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
                user_name = div.find(
                    'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd'}).get_text()
                date = soup.find('a',
                                 class_='css-4rbku5 css-18t94o4 css-901oao r-m0bqgq r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')
                date = str(date)
                dateSta = str(date).find('datetime') + 10
                dateSto = str(date).find('">', dateSta)
                date = date[dateSta:dateSto]
                date = date[0:10]  # yyyy-mm-dd
                content = div.find('div', {
                    'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}).descendants
                contentData = ''
                flagi = True
                for j in content:
                    if flagi:
                        flagi = False
                        contentData += str(j.string)
                    else:
                        flagi = True
                contentData = contentData.strip().replace('\n', '')
            except:
                print("获取数据错误一次")
            try:
                # 数据库部分:先查找，如果没有，则插入；如果有，
                # 查找
                name = name.replace('"', '')
                user_name = user_name.replace('"', '')
                date = date.replace('"', '')
                contentData = contentData.replace('"', '')

                chaZhao = "select * from twtable1 where content = " + '"' + contentData + '"'  # 引号
                cur.execute(chaZhao)
                curRetData = cur.fetchall()
                if len(curRetData) != 0:  # 有数据
                    pass
                else:  # 无数据
                    buyKeyWords = ["get", "pay", "take", "shop", "bribe", "cheap", "obtain", "accept", "payoff",
                                   "believe",
                                   "acquire", "bargain", "redeem", "procure", "purchase"]
                    buyKeyWord_list = []
                    for buyKeyWord in buyKeyWords:
                        if buyKeyWord in contentData:
                            buyKeyWord_list.append('1')
                        else:
                            buyKeyWord_list.append('0')
                    chaRuSql = 'INSERT INTO twtable1 (name,user_name,date,content,buy_get,pay,take,shop,bribe,cheap,obtain,accept,payoff,believe,acquire,bargain,redeem,procure,purchase) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                        name, user_name, date, contentData, buyKeyWord_list[0], buyKeyWord_list[1], buyKeyWord_list[2],
                        buyKeyWord_list[3], buyKeyWord_list[4], buyKeyWord_list[5], buyKeyWord_list[6],
                        buyKeyWord_list[7], buyKeyWord_list[8], buyKeyWord_list[9], buyKeyWord_list[10],
                        buyKeyWord_list[11], buyKeyWord_list[12], buyKeyWord_list[13], buyKeyWord_list[14])
                    cur.execute(chaRuSql)  # 执行sql语句
                    conn.commit()  # 提交到数据库执行



            except Exception as e:
                # traceback.print_exc()
                # print('traceback.format_exc%s' % traceback.format_exc())
                print("数据提交到数据库错误一次")
    pass


def conMySQL():
    try:
        conn = pymysql.connect(host='localhost', user='root', port=3306, passwd='123456', db='twitterdata',
                               charset='utf8')
        return conn, True
    except:
        print("连接数据库失败")


def allProcess():
    # 打开浏览器
    driver = openChrome()
    conn, connFlag = conMySQL()
    if connFlag:
        # 开始爬取
        getData(driver, conn)


if __name__ == '__main__':
    print("Start at:", time.asctime(time.localtime(time.time())))
    keyword = "mask"
    allProcess()
    print("Stop at:", time.asctime(time.localtime(time.time())))
