import scrapy
from datetime import datetime
import nltk
import datetime
import logging

class DebugSpider(scrapy.Spider):
    name = "DebugSpider"
    results = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        print('hello world')
        nltk.download('punkt')
        for url in self.start_urls:
            print('parsing blog %s' % url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not response.xpath('//title'):
            yield scrapy.Request(url=response.url, dont_filter=True)

        blog_url = response.url
        title = response.selector.xpath(self.config['title_xpath']).extract()
        date = response.selector.xpath(self.config['date_xpath']).extract()
        blog_info = response.selector.xpath(self.config['blog_paragraphs_xpath']).extract()

        if 'parse_date_string' in self.config:
            date_obj = datetime.datetime.strptime(date[0][:self.config['parse_date_string']], self.config['date_format'])
        else:
            date_obj = datetime.datetime.strptime(date[0].strip(), self.config['date_format'])

        print('MIKE - Date Obj: {0}'.format(date_obj))
        print(title)
