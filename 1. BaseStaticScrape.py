import sys
from spiders import BaseSpider as BaseSpider
from scrapy.crawler import CrawlerProcess
import os
import requests
from lxml.html import fromstring
from scrapy.utils.project import get_project_settings
import yaml

configurations = [
    'android_malice',
    'android_malicious',
    'android_malware',
    'google_malice',
    'google_malicious',
    'google_malware',
    'play_store_malice',
    'play_store_malicious',
    'play_store_malware',
    'playstore_malice',
    'playstore_malicious',
    'playstore_malware',
]

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Brapy.settings'

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    for c in configurations:
        config_file = open(os.path.join(main_dir, 'config', 'static_config_{0}.yaml'.format(c)), 'r', encoding='UTF-8')
        config = yaml.load(config_file)

        for company_name in config:
            initial_scrape_config = config[company_name]['initial_scrape']
            download_directory = os.path.join(main_dir, 'temp', 'base_urls_for_keywords', '{0}_urls'.format(c))
            if not os.path.isdir(download_directory):
                os.mkdir(download_directory)

            performBaseProjectScrape(download_directory = download_directory, initial_configuration = initial_scrape_config, process = process, company_name = company_name)

    process.start()

def performBaseProjectScrape(download_directory, initial_configuration, company_name, process):
    base_spider = BaseSpider.BaseSpider()
    process.crawl(base_spider, config=initial_configuration, download_directory = download_directory, company_name = company_name, results = [])

def reupdate_proxies(main_dir):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    f = open(main_dir + '/config/proxylist.txt', 'w')
    f.truncate(0)
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = "https://" + ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            f.write(proxy + '\n')
    f.close()

    print("Finished scraping currently existing proxies")
    return proxies

if __name__== "__main__":
    main()
