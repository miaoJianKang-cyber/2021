from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

brower = webdriver.Chrome()
brower.get("http://www.baidu.com")
try:
    brower.get("http://www.baidu.com")
    input = brower.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(brower, 10)
    # wait.until(EC.presence_of_all_elements_located(By.ID, 'content_left'))
    print(brower.current_url)
    print(brower.get_cookies())
    print(brower.page_source)
finally:
    brower.close()
