from urllib import response
from bs4 import BeautifulSoup
import requests

def request_maoyan(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.146 Safari/537.36',
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def main():
    url = 'https://vip.fxxkpython.com/?p=1891'
    html = request_maoyan(url)
    soup = BeautifulSoup(html, 'lxml')
    print(soup.get_text())

main()