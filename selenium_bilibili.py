from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt


option = webdriver.ChromeOptions()
# option.binary_location = r'C:\Program Files (x86)\Microsoft\EdgeCore\105.0.1343.25\msedge.exe'
# browser = webdriver.Edge(r'E:\Projects\Python\edgedriver_win64\msedgedriver.exe')
option.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
browser = webdriver.Chrome(r'E:\Projects\Python\chromedriver_win32\chromedriver.exe')

WAIT = WebDriverWait(browser, 10)
browser.get('https://www.bilibili.com/')

input = browser.find_element(By.CLASS_NAME, "nav-search-input")
input.send_keys("蔡徐坤")
input.submit()

all_h = browser.window_handles
browser.switch_to.window(all_h[1])
WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#server-search-app > div.contain > div.body-contain > div > div.result-wrap.clearfix')))
print(browser.find_element(By.CLASS_NAME, 'video-list row'))

# WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'bili-video-card')))

# html = browser.page_source
# soup = BeautifulSoup(html, 'lxml')
# list = soup.find_all("bili-video-card")
# for item in list:
#     print(item)


