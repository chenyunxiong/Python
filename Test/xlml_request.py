import requests
from lxml import html

def get():
    page = requests.get("http://econpy.pythonanywhere.com/ex/001.html")
    tree = html.fromstring(page.text)
    buyers = tree.xpath('//dev[@title="buyer-name"]/text()')
    prices = tree.xpath('//span[@class="item-price"]/text()')
    print ("buyers:", buyers)
    print ("price:", prices)
get()