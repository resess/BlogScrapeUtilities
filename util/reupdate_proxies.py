import requests
from lxml.html import fromstring
import os

def main():
    util_dir = os.path.dirname(os.path.realpath(__file__))
    reupdateProxies(os.path.join(util_dir, '..'))

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


if __name__ == "__main__":
    main()
