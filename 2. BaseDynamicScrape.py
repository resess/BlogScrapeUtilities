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
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'Brapy.settings'

    for c in configurations:
        config_file = open(os.path.join(main_dir, 'config', 'dynamic_config_{0}.yaml'.format(c)), 'r', encoding='UTF-8')
        config = yaml.load(config_file)
        download_directory = os.path.join(main_dir, 'temp', 'base_urls_for_keywords', '{0}_urls'.format(c))

        if not os.path.isdir(download_directory):
            os.mkdir(download_directory)

        for company_name in config:
            company_config = config[company_name]
            print(company_config['search_link'])
            results = run_company_driver(config=config[company_name], company_name = company_name, main_dir = main_dir)

            if len(results) > 0:
                file = open(os.path.join(download_directory, company_name + 'Blogs.txt'), 'w+')
                file.truncate(0)

                for url in results:
                    file.write(url + '\n')

                print(company_name + ': saving base_scrape_output to' + os.path.join(download_directory, company_name + 'Blogs.txt') + '\n')
                file.close()

def run_company_driver(config, company_name, main_dir):
    print('Starting selenium crawl for ' + company_name)
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=main_dir+'/drivers/geckodriver.exe')
    # driver = webdriver.Chrome(options = options, executable_path=main_dir+'/drivers/chromedriver.exe')

    if 'search_action_config' in config:
        perform_pre_search_actions(driver = driver, config = config['search_action_config'], max_timeout = config['max_timeout'], search_link = config['search_link'])
        print('yes')
    else:
        driver.get(config['search_link'])

    results = perform_page_scrape(driver = driver, config = config['page_scrape_config'], max_timeout = config['max_timeout'], original_url = config['search_link'], max_page_limit = config['max_page_limit'], delay = config['suitable_page_wait_time'])

    print('results')
    for item in results:
        print(item)

    print('Closing selenium crawl for ' + company_name)
    driver.close()
    return results

def perform_page_scrape(driver, config, max_timeout, original_url, max_page_limit, delay):
    results = set()
    current_pages_scraped = 1

    while True:
        time.sleep(delay)
        html_source = driver.page_source
        parser = fromstring(html_source)

        next_page = parser.xpath(config['next_page_xpath'])
        current_urls = parser.xpath(config['page_links_xpath'])

        for url in current_urls:
            if url.startswith('/'):
                parsed_uri = urlparse(original_url)
                result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                result_url = result + url
            else:
                result_url = url

            results.add(result_url)

        if current_pages_scraped >= max_page_limit:
            time.sleep(delay)
            break
        elif len(next_page) <= 0 or not driver.find_element_by_xpath(config['next_page_xpath']).is_enabled() or not driver.find_element_by_xpath(config['next_page_xpath']).is_displayed():
            print('found no next button')
            time.sleep(delay)
            break
        else:
            time.sleep(2)
            element = WebDriverWait(driver, max_timeout).until(EC.presence_of_element_located((By.XPATH, config['next_page_xpath'])))
            element.click()
            wait_for_ajax_calls(driver)

            current_pages_scraped += 1

    return results

def perform_pre_search_actions(driver, config, max_timeout, search_link):
    driver.get(search_link)
    for key in config:
        action = config[key]['action']

        if action == 'click and fill':
            element_xpath = config[key]['element_xpath']
            element_value = config[key]['element_value']

            print('looking for element located at ' + element_xpath)
            element = WebDriverWait(driver, max_timeout).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
            print('found element!')
            element.click()
            element.send_keys(element_value)
            print('performing click on element ' + element_xpath)
        elif action == 'wait':
            element_value = config[key]['element_value']
            time.sleep(element_value)
            print('performing wait for ' + str(element_value) + ' seconds.')
        elif action == 'click':
            element_xpath = config[key]['element_xpath']

            print('looking for element located at ' + element_xpath)
            element = WebDriverWait(driver, max_timeout).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
            print('found element!')

            element.click()

            wait_for_ajax_calls(driver)
        else:
            perform_pre_search_actions(driver, config, max_timeout, search_link)
            print('unknown action. restarting search')
            return

def wait_for_ajax_calls(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass

if __name__== "__main__":
    main()
