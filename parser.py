from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import json
class Parser(ABC):
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'Accept-Language': 'en-US'
    }
    __slot__ = ['_url']
    def __init__(self, url):
        self._url = url
    def get_soup(self):
        res = requests.get(self._url, headers=Parser._HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        return soup
    @abstractmethod
    def get_product_data(self):
        pass

class AmazonParser(Parser):
    def get_product_data(self):
        soup = self.get_soup()
        product_data = soup.find("div",class_='a-section aok-hidden twister-plus-buying-options-price-data').get_text()
        title = soup.find(id="productTitle").get_text().strip()
        price = json.loads(product_data)[0]["displayPrice"]
        return json.dumps({"title": title, "price": price})
class EbayParser(Parser):
    def get_product_data(self):
        soup = self.get_soup()
        title = soup.find('title').get_text().strip("| eBay").strip()
        price = "$"+soup.find(id='prcIsum')['content']
        return json.dumps({"title": title, "price": price})
     
if __name__ == "__main__":
    amazon = AmazonParser("https://www.amazon.com/Anker-Aluminum-Pixelbook-Compatible-Thunderbolt/dp/B07THJGZ9Z/?_encoding=UTF8&pd_rd_w=moCuR&pf_rd_p=5fe95cd4-8512-42fa-bf21-63d83b898785&pf_rd_r=GDT6TK7W9SF8P507778T&pd_rd_r=aa811c73-e50c-4793-8248-0fd1b1102999&pd_rd_wg=bOFVG&ref_=pd_gw_ci_mcx_mr_hp_atf_m")
    ebay = EbayParser("https://www.ebay.com/itm/294510289616?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20200708143445%26meid%3Df223ab7979a449f6aef0f98042c14f26%26pid%3D101251%26rk%3D1%26rkt%3D1%26itm%3D294510289616%26pmt%3D0%26noa%3D1%26pg%3D2380057%26algv%3DPersonalizedTopicsV2WithMetaOrganicPRecall&_trksid=p2380057.c101251.m47269&_trkparms=pageci%3A94a67767-dbaf-11ec-ac0f-b2041c261ee8%7Cparentrq%3Af827598f1800a764ad801049ffffb80e%7Ciid%3A1")
    print(amazon.get_product_data())
    print(ebay.get_product_data())
    
    