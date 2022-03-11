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
output_file_name = 'allblogs_fifthrun'

def clean_up(x):
    return str(x).strip()

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Brapy.settings'

    static_config_file = open(os.path.join(main_dir, 'config', 'singulartestconfig.yaml'), 'r', encoding='UTF-8')
    static_config = yaml.load(static_config_file)

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    url_lists_to_ignore_df = pd.read_excel(os.path.join(main_dir, 'temp', 'blog_scrape_output', 'allblogs.xlsx'))
    url_lists_to_ignore_df['blog_content'] = url_lists_to_ignore_df['blog_info_concat'].apply(lambda x: clean_up(x))
    url_lists_to_ignore_df.to_excel(os.path.join(main_dir, 'temp', 'blog_scrape_output', 'allblogs_clean.xlsx'))
    exit(0)

    url_lists_to_ignore = set()
    if os.path.isfile(os.path.join(main_dir, 'temp', 'blog_scrape_output', 'allblogs_merged.xlsx')):
        url_lists_to_ignore_df = pd.read_excel(os.path.join(main_dir, 'temp', 'blog_scrape_output', 'allblogs_merged.xlsx'))
        for url in url_lists_to_ignore_df['blog_url'].values:
            url_lists_to_ignore.add(url)

    if not os.path.isfile(os.path.join(main_dir, 'temp', 'AllBlogs.xlsx')):
        print('Cannot find: {0}'.format(os.path.join(main_dir, 'temp', 'AllBlogs.xlsx')))
        exit(-1)
    else:
        all_blogs_df = pd.read_excel(os.path.join(main_dir, 'temp', 'AllBlogs.xlsx'))
        print(all_blogs_df.columns.values)

        for company in sorted(all_blogs_df['company'].unique()):
            if company  in static_config:
                company_blogs = all_blogs_df[all_blogs_df['company'] == company]
                out_file = os.path.join(main_dir, 'temp', 'detailscrape5', '{0}.txt'.format(company))
                urls_left = 0

                urls_to_get = set()
                for url in company_blogs['url'].values:
                    if url not in url_lists_to_ignore:
                        urls_left += 1
                        urls_to_get.add(url)

                if len(urls_to_get) > 0:
                    print(urls_to_get)

                print('{0} => {1}, before: {2}'.format(company, urls_left, len(company_blogs['url'].values)))
                list_to_txt(out_file, urls_to_get)
            else:
                print('{0} not found in config'.format(company))
                exit(-1)
            # print(company.strip())

    #clean_up_directory(main_dir + '/temp/blog_scrape_output')
    for company_name in static_config:
        blog_scrape_config = static_config[company_name]['blog_scrape']

        blog_file = os.path.join(main_dir, 'temp', 'detailscrape5', company_name + '.txt')

        print(blog_file)
        if os.path.exists(blog_file):
            print('FOUND')
            performBlogScrape(blogs_file = blog_file, blog_scrape_config = blog_scrape_config, company_name = company_name, process = process, main_dir = main_dir)

    '''
    for company_name in custom_config:
        blog_scrape_config = custom_config[company_name]['blog_scrape']
        download_directory = main_dir + '/temp/base_scrape_output/'

        blog_file = main_dir + '/temp/base_scrape_output/' + company_name + 'Blogs.txt'
        if os.path.exists(blog_file):
            performBlogScrape(blogs_file = blog_file, blog_scrape_config = blog_scrape_config, company_name = company_name, process = process, main_dir = main_dir)
    '''

    process.start()
    saveSpiderOutput(main_dir=main_dir)

def list_to_txt(output_file, list):
    file = open(output_file, "w")
    file.truncate(0)

    for item in list:
        file.write(item + '\n')

def saveSpiderOutput(main_dir):
    columns = ['title', 'date', 'blog_url', 'matches', 'blog_info_concat', 'company']
    df = pd.DataFrame(columns=columns)
    writer = ExcelWriter(os.path.join(main_dir, 'temp', 'blog_scrape_output', output_file_name + '.xlsx'))

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
