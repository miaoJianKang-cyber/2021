from selenium import  webdriver #从这个selenium导入web的引擎或者接口
import time
duixiang = webdriver.Chrome()
duixiang.implicitly_wait(5)
duixiang.get('http://f.python3.vip/webauto/sample2.html')

duixiang.switch_to.frame('frame1') #页面里面嵌套页面，这样可以做是跳转到嵌套页里面，frame1是ID的值或者先name的值
yuansu = duixiang.find_element_by_css_selector('span')
print(yuansu.get_attribute('outerHTML'))
duixiang.switch_to.default_content()  #这个是退出嵌套页面

duixiang.find_element_by_id('outerbutton').click() #点击里面的按钮
