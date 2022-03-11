import sys
from spiders import BlogSpider as BlogSpider
from scrapy.crawler import CrawlerProcess
import os
import requests
from lxml.html import fromstring
from scrapy.utils.project import get_project_settings
import yaml
from pandas import ExcelWriter
import os
import pandas as pd

spiders = []
output_file_name = 'all_merged_second_try'

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Brapy.settings'

    static_config_file = open(os.path.join(main_dir, 'config', 'static_config.yaml'), 'r', encoding='UTF-8')
    static_config = yaml.load(static_config_file)
    dynamic_config_file = open(os.path.join(main_dir, 'config', 'dynamic_config.yaml'), 'r', encoding='UTF-8')
    dynamic_config = yaml.load(dynamic_config_file)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # clean_up_directory(main_dir + '/temp/blog_scrape_output')
    for company_name in static_config:
        blog_scrape_config = static_config[company_name]['blog_scrape']

        blog_file = main_dir + '/temp/blog_scrape_output_merged/' + company_name + 'Blogs.txt'

        print(blog_file)
        if os.path.exists(blog_file):
            performBlogScrape(blogs_file = blog_file, blog_scrape_config = blog_scrape_config, company_name = company_name, process = process, main_dir = main_dir)

    for company_name in dynamic_config:
        # if company_name == 'Checkpoint':
        blog_scrape_config = dynamic_config[company_name]['blog_scrape']

        blog_file = main_dir + '/temp/blog_scrape_output_merged/' + company_name + 'Blogs.txt'
        if os.path.exists(blog_file):
            performBlogScrape(blogs_file = blog_file, blog_scrape_config = blog_scrape_config, company_name = company_name, process = process, main_dir = main_dir)

    process.start()
    saveSpiderOutput(main_dir=main_dir)

def saveSpiderOutput(main_dir):
    columns = ['title', 'date', 'blog_url', 'matches', 'company']
    df = pd.DataFrame(columns=columns)
    writer = ExcelWriter(main_dir + '/temp/blog_scrape_output/' + output_file_name + '.xlsx')

    for spider in spiders:
        company_name = spider[0]

        for blog_collection in spider[1].results:
            if blog_collection[0] == company_name:
                blog_collection[1].append(str(company_name).strip())
                df.loc[len(df)] = blog_collection[1]

    df.to_excel(writer, 'All Companies')
    writer.save()

def clean_up_directory(dir):
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def performBlogScrape(blogs_file, blog_scrape_config, company_name, process, main_dir):
    blog_links = []
    with open(blogs_file, 'r') as blogFile:
        row = blogFile.readlines()
        for url in row:
            if url:
                blog_links.append(url.strip())

    if len(blog_links) > 0:
        blog_spider = BlogSpider.BlogSpider()
        process.crawl(blog_spider, start_urls = blog_links, config = blog_scrape_config, company_name = company_name, results = [], main_dir = main_dir)
        spiders.append([company_name, blog_spider])
    else:
        print('Nothing to parse in blog file ' + blogs_file)

def reupdateProxies(mainDir):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    f = open(mainDir + '/config/proxylist.txt', 'w')
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
