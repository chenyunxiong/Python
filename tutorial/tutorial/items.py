# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GeekDocItem(scrapy.Item):
    title = scrapy.Field()
    subList = scrapy.Field()

class GeekDocSubItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class BossscrapyItem(scrapy.Item):
    url = scrapy.Field()
    jobs = scrapy.Field()
    work_address = scrapy.Field()
    scalary = scrapy.Field()
    experiences = scrapy.Field()
    degree = scrapy.Field()
    company = scrapy.Field()
    financing_condition = scrapy.Field()
    company_persion = scrapy.Field()