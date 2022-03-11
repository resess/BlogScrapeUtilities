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

def main():
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Brapy.settings'

    blog_out_dir = os.path.join(main_dir, '..', 'temp', 'out')

    print(blog_out_dir)
    result_df = pd.DataFrame()
    for root, dirs, files in os.walk(blog_out_dir, topdown=False):
        for name in files:
            if name.endswith('.xlsx'):
                print(name)

                df = pd.read_excel(os.path.join(root, name))
                result_df = result_df.append(df, ignore_index=True)


    print(result_df)
    output_file = os.path.join(main_dir, '..', 'temp', 'out', 'output_new.xlsx')
    if not os.path.isfile(output_file):
        result_df.to_excel(output_file)



if __name__== "__main__":
    main()
