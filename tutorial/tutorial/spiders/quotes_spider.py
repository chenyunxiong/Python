import scrapy
import xlwt

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    exl = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = exl.add_sheet("名人名言", cell_overwrite_ok=True)
    sheet.write(0, 0, "author")
    sheet.write(0, 1, "words")
    page_index = 0
    row, column = 1, 0
    
    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            # 'https://quotes.toscrape.com/page/2/',
            # 'http://woodenrobot.me'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('title::text')[0].get()
        self.page_index += 1
        # sheet = self.exl.add_sheet("第%s页"%self.page_index, cell_overwrite_ok=True)
        # sheet.write(0, 0, "author")
        # sheet.write(0, 1, "words")
        quotes = response.css('div.quote')
        for item in quotes:
            text = item.css('span.text::text').get()
            self.sheet.write(self.row, self.column, text)
            self.column += 1
            author = item.css('small.author::text').get()
            self.sheet.write(self.row, self.column, author)
            self.column = 0
            self.row += 1
            print("t: ", text, author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page != None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        self.exl.save('名人名言.xlsx')

        # queue = response.css('div.quote')[0]
        # print("t: ", queue.css('span.text::text').get())

        # print(".........:",response.text)
        # texts = response.css('title::text')[0].get()#.xpath('//text/text()')
        # for txt in texts:
        #     print(txt)

        # page = response.url.split("/")[-2]
        # print(page)
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as file:
        #     file.write(response.body)
        # self.log(f'Saved file {filename}')