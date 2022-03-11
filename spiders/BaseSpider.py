import scrapy
import time
import random
import requests
from lxml.html import fromstring
from urllib.parse import urlparse
import os

class BaseSpider(scrapy.Spider):
    name = "BaseSpider"
    currentPagesScraped = 0

    def __init__(self, **kwargs):
        self.project_urls = []
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        print(self)
        url = self.config['search_link']
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not response.xpath('//title'):
            yield scrapy.Request(url=response.url, dont_filter=True)

        parser = fromstring(response.text)

        next_page = parser.xpath(self.config['next_page_xpath'])
        current_urls = parser.xpath(self.config['page_links_xpath'])

        for url in current_urls:
            if url.startswith('/'):
                parsed_uri = urlparse(response.url)
                result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                result_url = result + url
            else:
                result_url = url

            self.project_urls.append(result_url)

        self.currentPagesScraped += 1
        if ((self.currentPagesScraped < self.config['max_pages_to_scrape']) and len(next_page) == 1):
            next_url = next_page[0]

            if (next_page[0].startswith('/')):
                parsed_uri = urlparse(response.url)
                result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                next_url = result + next_page[0]
                print(next_url)

            print(self.company_name + ': scraping next page ' + next_url + '...')
            yield scrapy.Request(url = next_url, callback = self.parse)
        else:
            if len(self.project_urls) > 0:
                file = open(os.path.join(self.download_directory, self.company_name + 'Blogs.txt'), 'w+')
                file.truncate(0)

                for url in self.project_urls:
                    file.write(url + '\n')

                print(self.company_name + ': saving base_scrape_output to' + self.download_directory + self.company_name + 'Blogs.txt' + '\n')
                file.close()

            print(self.company_name + ': max pages reached. Done scraping.')
