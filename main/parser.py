from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import json
import sys
import re

class Parser(ABC):
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'Accept-Language': 'en-US'
    }
    def get_soup(self, url):
        res = requests.get(url, headers=Parser._HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        return soup
    @abstractmethod
    def get_product_data(self):
        pass

class AmazonParser(Parser):
    def get_product_data(self, url):
        soup = self.get_soup(url)
        product_data = soup.find("div",class_='a-section aok-hidden twister-plus-buying-options-price-data').get_text()
        title = soup.find(id="productTitle").get_text().strip()
        price = json.loads(product_data)[0]["displayPrice"]
        return json.dumps({"title": title, "price": price})

class EbayParser(Parser):
    def get_product_data(self, url):
        soup = self.get_soup(url)
        title = soup.find('title').get_text().strip("| eBay").strip()
        price = "$"+soup.find(id='prcIsum')['content']
        return json.dumps({"title": title, "price": price})

class EtsyParser(Parser):
    def get_product_data(self, url):
        soup = self.get_soup(url)
        title = soup.find('title').get_text().strip("| Etsy").strip()
        price = soup.find('p', class_="wt-text-title-03 wt-mr-xs-2").get_text().strip()
        return json.dumps({"title": title, "price": price})

if __name__ == "__main__":
    dct = {}
    dct['amazon'] = AmazonParser
    dct['ebay'] = EbayParser
    dct['etsy'] = EtsyParser
    url = sys.argv[1]
    site = re.findall(r'www\..+\.com', url)[0].strip('www.').strip('.com')
    print(dct[site]().get_product_data(url))
