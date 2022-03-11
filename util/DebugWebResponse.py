import sys
from spiders import DebugSpider as DebugSpider
from scrapy.crawler import CrawlerProcess
import os
import requests
from lxml.html import fromstring
from scrapy.utils.project import get_project_settings
import yaml
from pandas import ExcelWriter
import os
import pandas as pd

blog_links = ['https://research.checkpoint.com/2021/clast82-a-new-dropper-on-google-play-dropping-the-alienbot-banker-and-mrat/']
company_name = 'Checkpoint'
tag = 'android_malware'

main_dir = os.path.dirname(os.path.realpath(__file__) + '/..' + '/..' + '/..')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

static_config_file = open(os.path.join(main_dir, 'config', 'dynamic_config_{0}.yaml'.format(tag)), 'r', encoding='UTF-8')
blog_scrape_config = ((yaml.load(static_config_file))[company_name])['blog_scrape']

settings = get_project_settings()
process = CrawlerProcess(settings)

debug_spider = DebugSpider.DebugSpider()
process.crawl(debug_spider, start_urls=blog_links, config=blog_scrape_config, company_name=company_name, results=[], main_dir=main_dir)

process.start()