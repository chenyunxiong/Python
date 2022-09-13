# -*- coding: utf-8 -*-
import scrapy
import logging
from tutorial.items import BossscrapyItem

class BossscrapySpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    prefix_url = 'http://www.zhipin.com/'
    start_urls = [
        'http://www.zhipin.com/'
    ]

    def __init__(self, name=None, **kwargs):
        self.url = 'https://www.zhipin.com/101230100/?page={pageNo}&ka=page-{pageNo}&query=心理'
        self.now_page = 1
        super().__init__(name, **kwargs)

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     return super().from_crawler(crawler, *args, **kwargs)
    #
    def start_requests(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
        }
        cookie = {
            'Cookie': 'lastCity=101230100; __zp_seo_uuid__=ecffedd2-4c57-4ed1-8b8d-07185d299800; __g=-; wd_guid=27d73000-86d1-4054-8636-0146287f9f53; historyState=state; _bl_uid=e7lkj7hyz02m38wnwyFLqUR5psR6; wt2=DFpmT_nWD4ttXT0IZlnqoDYHoH_mHEdd23nGwnUf7LHqLOFdhZ74TyOC0c_etWW1sRGZZp3oU_MDmrKeR7dKYqw~~; wbg=0; __c=1663039467; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E5%25BF%2583%25E7%2590%2586%26city%3D101230100&s=3&g=&friend_source=0&s=3&friend_source=0; __a=27620412.1663039467..1663039467.8.1.8.8; geek_zp_token=V1SN8lFOz821tgXdNvzB0cKCyx7TjXwA~~; __zp_stoken__=62b5eaTwjaDxeECRQXC5NQVtYHHk6cU0uSCopUAM6cnIJVTwMLyY6TkoQOzIBX30kJm4JB2xEImR2ZzsYTQJ2BQdJaXI5VnRvTwFxV3M9AnpSCQUqJRtOFCl0P0w7QjAnZFc7Dj9OXUdgPGE%3D'
        }
        yield scrapy.Request(self.url.format(pageNo=self.now_page), headers=header, cookies=cookie, callback=self.parse,)


    def parse(self, response):
        global degree
        global company_persion
        logging.info(response)
        item = BossscrapyItem()
        if bool(response.xpath("//div[@class='job-list']")) == False:
            logging.info('cookie已失效')
            return
        for info in response.xpath("//div[@class='job-list']/ul//li"):
            url = self.prefix_url + ''.join(info.xpath(".//span[@class='job-name']/a/@href").extract())
            jobs = ''.join(info.xpath(".//span[@class='job-name']/a/text()").extract())
            work_address = info.xpath(".//span[@class='job-area']/text()").get()
            scalary = info.xpath(".//div[@class='job-limit clearfix']/span/text()").get()
            if len(info.xpath(".//div[@class='job-limit clearfix']/p/text()").extract()) == 2:
                experiences, degree = info.xpath(".//div[@class='job-limit clearfix']/p/text()").extract()
            else:
                experiences = ''.join(info.xpath(".//div[@class='company-text']/p/text()").extract())
            company = ''.join(info.xpath(".//div[@class='company-text']/h3/a/text()").extract())
            if len(info.xpath(".//div[@class='company-text']/p/text()").extract()) == 2:
                financing_condition,company_persion = info.xpath(".//div[@class='company-text']/p/text()").extract()
            else:
                financing_condition = ''.join(info.xpath(".//div[@class='company-text']/p/text()").extract())
            item['url'] = url
            item['jobs'] = jobs
            item['work_address'] = work_address
            item['scalary'] = scalary
            item['experiences'] = experiences
            item['degree'] = degree
            item['company'] = company
            item['financing_condition'] = financing_condition
            item['company_persion'] = company_persion
            yield item
        try:
            page = response.xpath("//div[@class='page']/a[last()]/@href").get()
            next_url = self.prefix_url + page
            if not page:
                logging.info("爬取完毕，退出爬虫")
                return
            else:
                logging.info("下一页地址：{}".format(next_url))
                yield scrapy.Request(next_url)

        except Exception as e:
            logging.info('爬虫异常，退出爬虫...{}'.format(e))
            return



# import scrapy


# class BossSpider(scrapy.Spider):
#     name = 'boss'
#     allowed_domains = ['www.zhipin.com']
#     start_urls = ['https://www.zhipin.com/web/geek/job?query=心理&city=101230100&page=2']

#     def start_requests(self):
#         header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27',
#         }
#         cookie = {
#             'Cookie': 'lastCity=101230100; __zp_seo_uuid__=7d90662e-43db-4806-9c55-49d7fc3b8185; __c=1663039467; __g=-; __l=r=https%3A%2F%2Fcn.bing.com%2F&l=%2Fwww.zhipin.com%2Ffuzhou%2F&s=1&g=&s=3&friend_source=0; __a=27620412.1663039467..1663039467.1.1.1.1'
#         }
#         print(".......a")
#         yield scrapy.Request(url=self.start_urls[0], cookies=cookie, headers=header, callback=self.parse)
    
#     def parse(self, response):
#         mainTitle = response.xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/div[1]')
#         print("t:", mainTitle)
