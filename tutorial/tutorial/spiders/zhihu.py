from http import cookies
from wsgiref import headers
import scrapy

# Cookie添加正确可爬  
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/question/531148965/answer/2470885305']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        cookies = {
            'Cookie':''
        }
        yield scrapy.Request(url=self.start_urls[0], cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        print("t:", response.text)
