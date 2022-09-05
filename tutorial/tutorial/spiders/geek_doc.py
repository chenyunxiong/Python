import imp
import scrapy
from scrapy import Selector

from tutorial.items import GeekDocItem
from tutorial.items import GeekDocSubItem
import xlwt

class GeekDocSpider(scrapy.Spider):
    name = 'geek_doc'
    allowed_domains = ['geek-docs.com']
    start_urls = ['http://geek-docs.com/']

    def parse(self, response):
        mainTitle = response.xpath('/html/head/meta[4]')
        print('mainTitle: ', mainTitle)
        list = response.xpath('//div[@class=\'item\']')
        # book = xlwt.Workbook(mainTitle)
        # sheet = book.add_sheet(mainTitle)
        # sheet.write(0, 1, "大类")
        # sheet.write(0, 2, "子类")
        # print('items:',items)
        for v in list:
            item = GeekDocItem()
            item['title'] = v.xpath("h2/text()").get()
            print("subTitle: ", item['title'])
            subList = v.xpath('ul/li')
            item['subList'] = [10]
            sub = []
            for s in subList:
                subItem = GeekDocSubItem()
                subItem['title'] = s.xpath('a/@title').extract()
                subItem['link'] = s.xpath('a/@href').extract()
                subItem['desc'] = s.xpath('a/text()').extract()
                print("subT: ", subItem['title'])
                print("sublink: ", subItem['link'])
                print("subdesc: ", subItem['desc'])
                sub.append(subItem)
            item['subList'] = sub
            yield item

        
            
