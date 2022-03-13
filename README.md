# BlogCrawler
This repository hosts an implementation of a web crawler which contains capabilities to scrape contents of blog posts from security related companies.

## Pre-requisites

- Python 3.6
- NumPy 1.14+
- Pandas 0.23+
- Selenium 3.141
- Scrapy 1.7.3

## Configuration Instructions

1. Modify settings.py to set USER_AGENT_LIST + PROXY_LIST to the project's metainfo useragents.txt and proxylist.txt
2. Create configurations under [GithubProject]/config

For blogs which contain __AJAX components__, create a new dynamic configuration with a file name of your choice. Fill in the following yaml keys:

- search_link = blog home page
- search_action_config = actions performed before the scraping process (ex. click, click and fill)
- page_scrape_config = xpath configuration to locate the blog article links (page_links_xpath) and next page indicator (next_page_xpath)
- blog_scrape = xpath configuration used to scrape each blog article

For blogs which can be scraped __statically__, create a new static configuration with a file name of your choice. Fill in the following yaml keys:

- search_link = blog home page
- page_scrape_config = xpath configuration to locate the blog article links (page_links_xpath) and next page indicator (next_page_xpath)
- blog_scrape = xpath configuration used to scrape each blog article

## Running Instructions

1. Create static/dynamic configuration files using the configuration instructions above. Refer to existing configurations for reference
2. Modify BaseStaticScrape.py/BaseDynamicScrape.py to only include the filename of the configuration(s) you would like to run.
3. Run BaseStaticScrape.py + BaseDynamicScrape.py
4. Run BlogScrape.py
5. Results will be written under the [GithubProject]/temp folder
