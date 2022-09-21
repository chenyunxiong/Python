# 大图网爬图
import os
import requests
from bs4 import BeautifulSoup

def request_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
    except:
        return None


def get_page_url():
    for i in range(1, 4):
        baseUrl = 'http://www.daimg.com/photo/list_4_{}.html'.format(i)
        print("url2: ", baseUrl)
        html = request_page(baseUrl)
        if html == None:
            continue
        soup = BeautifulSoup(html, 'lxml')
        elements = soup.find(class_='ibox2_list').find_all('li')
        urls = []
        for item in elements:
            url = item.find("a").get('href')#.find('img').get('src')
            urls.append(url)
        return urls

def download(urls):
    if os.path.exists('imgs'):
        os.removedirs('imgs')
    os.makedirs('imgs')
    for url in urls:
        html = request_page(url)
        if html == None:
            continue
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find(class_='n_img').find("img").get('title')
        src = soup.find(class_='n_img').find("img").get('src')
        filename = 'imgs/%s.jpg' % title
        print('url', filename)
        with open(filename, 'wb') as file:
            img = requests.get(src).content
            file.write(img)

if __name__ == '__main__':
    urls = get_page_url()
    download(urls)
