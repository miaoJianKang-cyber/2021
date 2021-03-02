from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
opt.add_argument('window-size=1920x3000')       # 设置浏览器分辨率
opt.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
opt.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
opt.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
opt.add_argument('--headless')                  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
 # opt.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" # 手动指定使用的浏览器位置
driver = webdriver.Chrome(options=opt)          # 创建无界面对象
driver.get('http://www.baidu.com')
print(driver.current_window_handle)
# print(driver.page_source)
driver.close()