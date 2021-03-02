import xlwings as xw

wb = xw.Book('TwitterData副本1.xlsx')
sht = wb.sheets[0]
rng = sht.range('a1').expand('table')

nrows = rng.rows.count  # 行数

name = sht.range('a1:a{}'.format(nrows)).value
user_name = sht.range('b1:b{}'.format(nrows)).value
date = sht.range('c1:c{}'.format(nrows)).value
content = sht.range('d1:d{}'.format(nrows)).value

# "买"的英文翻译
keyWords = ["get", "pay", "take", "shop", "bribe", "cheap", "obtain", "accept", "payoff", "believe", "acquire",
            "bargain", "redeem", "procure", "purchase"]

for line in content:
    for keyword in keyWords:
        if keyword in line:
            print(keyword + "---->" + line)
