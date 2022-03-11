import sys
import os
import yaml
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from lxml.html import fromstring
from urllib.parse import urlparse
import shutil

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
    'playstore_malware'
]

def main():
    company_results = []
    main_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

    base_scrape_output_dir = os.path.join(main_dir, 'temp', 'base_urls_for_keywords')
    output_dir = os.path.join(main_dir, 'temp', 'blog_scrape_output_merged')
    companies = {}

    if os.path.isdir(base_scrape_output_dir):
        for root, dirs, files in os.walk(base_scrape_output_dir, topdown=False):
            for name in files:
                if name.endswith('.txt'):
                    c = os.path.join(root, name)

                    if name not in companies:
                        companies[name] = set()

                    with open(c) as f:
                        for line in f.readlines():
                            url = line.strip()
                            companies[name].add(url)


        for company in companies:
            print('{0}: {1}'.format(company, len(companies[company])))
            file = open(os.path.join(output_dir, company), 'w+')
            file.truncate(0)

            for url in companies[company]:
                print(url)
                file.write(url + '\n')

            file.close()
    else:
        print('{0} is not an existing directory'.format(base_scrape_output_dir))

if __name__== "__main__":
    main()
