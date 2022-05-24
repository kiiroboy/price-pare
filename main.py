import requests
from bs4 import BeautifulSoup
import json
import sys
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Accept-Language': 'en-US'
}

def get_amazon_product_price(url, headers):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    product_data = soup.find("div",class_='a-section aok-hidden twister-plus-buying-options-price-data').get_text()
    title= soup.find(id="productTitle").get_text().strip()
    print(title)
    for e in json.loads(product_data):
        if e["buyingOptionType"] == 'NEW':
            print("NEW", e["displayPrice"])
        else:
            print("USED", e["displayPrice"])

def get_ebay_product_price(url, headers):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    price = soup.find(id='prcIsum')['content']
    title = soup.find('title').get_text().strip("| eBay").strip()
    print(title)
    print(price)

if __name__=="__main__":
    if len(sys.argv) == 1:
        print("Usage: python main.py [url]")
        exit()
    dct = {}
    dct['amazon'] = get_amazon_product_price
    dct['ebay'] = get_ebay_product_price
    site = re.findall('www.[a-zAZ]+.com',sys.argv[1])[0].strip('www.').strip('.com')
    dct[site](sys.argv[1],headers)
