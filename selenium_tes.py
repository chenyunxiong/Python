import imp
from selenium import webdriver
from selenium.webdriver.common.by import By

option = webdriver.EdgeOptions()
option.binary_location = r'C:\Program Files (x86)\Microsoft\EdgeCore\105.0.1343.25\msedge.exe'
 

driver = webdriver.Edge(r'E:\Projects\Python\edgedriver_win64\msedgedriver.exe')
# driver.get('https://bing.com')
# element = driver.find_element(By.ID, 'sb_form_q')
# element.send_keys('WebDriver')
# element.submit()

driver.get('https://www.baidu.com')
element = driver.find_element(By.ID, 'kw')
element.send_keys('WebDriver')
element.submit()

button = driver.find_element_by_css_selector('#su')
button.click()