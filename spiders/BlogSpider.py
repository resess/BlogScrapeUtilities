import scrapy
from datetime import datetime
import nltk
import datetime

class BlogSpider(scrapy.Spider):
    name = "BlogSpider"
    results = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        nltk.download('punkt')
        analyzed = 0
        for url in self.start_urls:
            print('parsing blog %s' % url)
            yield scrapy.Request(url=url, callback=self.parse)
            analyzed += 1
            print('analyzed {0}/{1} blogs (%{2})'.format(analyzed, len(self.start_urls), (analyzed / len(self.start_urls)) * 100))

    def parse(self, response):
        blog_url = response.url
        title = response.selector.xpath(self.config['title_xpath']).extract()
        date = response.selector.xpath(self.config['date_xpath']).extract()
        blog_info = response.selector.xpath(self.config['blog_paragraphs_xpath']).extract()

        if 'parse_date_string' in self.config:
            date_obj = datetime.datetime.strptime(date[0][:self.config['parse_date_string']], self.config['date_format'])
        else:
            date_obj = datetime.datetime.strptime(date[0].strip(), self.config['date_format'])

        # concatenate all items in blog
        parsed_blog = ''

        for item in blog_info:
            parsed_blog += item

        # use natural language processing to split into sentences
        sentences = nltk.tokenize.sent_tokenize(parsed_blog)

        # match all keywords by converting to lower case
        key_words = [word.lower() for word in self.config['key_words'].split(',')]
        matches = []
        for sentence in sentences:
            if any(word in sentence.lower() for word in key_words):
                matches.append(sentence.strip())

        #output row
        BlogSpider.results.append([self.company_name,[title[0], date_obj, blog_url, matches]])