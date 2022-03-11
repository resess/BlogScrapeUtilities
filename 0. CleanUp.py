import sys
from spiders import BaseSpider as BaseSpider
from scrapy.crawler import CrawlerProcess
import os
import requests
from lxml.html import fromstring
from scrapy.utils.project import get_project_settings
import yaml

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

    # TODO: Initialize temp folders used for blog crawling process

if __name__== "__main__":
    main()
