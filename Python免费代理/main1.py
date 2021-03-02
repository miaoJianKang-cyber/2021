import requests
import parsel
import time, random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def get_ips():
    proxies_list = []
    for page in range(1, 2):
        # print("正在爬取第{}页的数据".format(str(page)))
        url = "https://www.kuaidaili.com/free/inha/{}".format(str(page))
        response = requests.get(url, headers=headers)
        data = response.text
        html_data = parsel.Selector(data)
        tr_parse = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        for tr in tr_parse:
            tmp_dict = {}
            Type = tr.xpath('./td[4]/text()').extract_first()
            IP = tr.xpath('./td[1]/text()').extract_first()
            PORT = tr.xpath('./td[2]/text()').extract_first()
            tmp_dict[Type] = IP + ":" + PORT
            # print(tmp_dict)
            proxies_list.append(tmp_dict)
        time.sleep(random.randint(1, 5))

    # print(proxies_list)
    # print("获取到的id的数量", len(proxies_list))
    return proxies_list


# 检查代理ip的可用性
def check_ip(proxies_list):
    can_use = []
    for pro in proxies_list:
        try:
            response = requests.get("https://www.baidu.com", headers=headers, proxies=pro, timeout=0.1)
            if response.status_code == 200:
                can_use.append(pro)
        except Exception as e:
            print(pro, e)
    return can_use


if __name__ == '__main__':
    proxies_list = get_ips()
    ips = check_ip(proxies_list)
    print("能用的ip", ips)
    print("能用的ip的数量", len(ips))
