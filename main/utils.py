from bs4 import BeautifulSoup
import requests
import json
import pytz
from django.utils import timezone
def get_link_data(url):
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        'Accept-Language': 'en-US'
    }
    res = requests.get(url, headers=_HEADERS)
    soup = BeautifulSoup(res.text, "lxml")
    logo_url = None
    if "www.amazon.com" in url:
        product_data = soup.find("div",class_='a-section aok-hidden twister-plus-buying-options-price-data').get_text()
        title = soup.find(id="productTitle").get_text().strip()
        price = json.loads(product_data)[0]["displayPrice"]
        img_div = soup.find(id="imgTagWrapperId")
        imgs_str = img_div.img.get('data-a-dynamic-image')
        logo_url = next(iter(json.loads(imgs_str)))
    elif "www.ebay.com" in url:
        title = soup.find('title').get_text().strip("| eBay").strip()
        price = "$"+soup.find(id='prcIsum')['content']
        img_lst = soup.find_all('img')
        for img in img_lst:
            logo_url = img['src']
            if 'i.ebayimg.com' in logo_url:
                break
    elif "www.etsy.com" in url:
        title = soup.find('title').get_text().strip("| Etsy").strip()
        price = soup.find('p', class_="wt-text-title-03 wt-mr-xs-2").get_text().strip()
        img_lst = soup.find('img', {'class':'wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded'})
        logo_url = img_lst['src']
    return title, price, logo_url


def convert_to_localtime(utctime):
    fmt = '%d/%m/%Y %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    print(timezone.now())
    return localtz.strftime(fmt)
if __name__ == "__main__":
    print(get_link_data("https://www.etsy.com/listing/1167979888/garden-of-love-personalized-round-garden?click_key=19d17f646325f4ca101188e6d866923a9fc638ef%3A1167979888&click_sum=893e8235&ref=hp_rv-4"))
