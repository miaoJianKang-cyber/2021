# coding:utf-8
from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.zhihu.com/explore")

# 将进度条下拉到最底部
# browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom")')

input = browser.find_element_by_class_name('ExploreRoundtableCard-questionTitle')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)