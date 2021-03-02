from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

driver=webdriver.Chrome()
driver.get("https://www.alibaba.com/product-detail/Mask-The-Mask-EN149-Disposable-Dust_60709522187.html")
teams = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="J-rich-text-description"]/p')))
print([i.text for i in teams])

driver.close()
driver.quit()