import requests
from bs4 import BeautifulSoup

URL = "https://markets.businessinsider.com/"
CURRENT_PRICE_SELECTOR = "#site > div > div:nth-child(2) > div.row.equalheights.greyBorder > div > div:nth-child(3) > div.col-sm-10.no-padding > div.col-xs-12.no-padding > div:nth-child(2) > span"


def get_stock_price(company_id):
    url = URL + "stocks/" + company_id + "-stock"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    price = str(soup.select_one(CURRENT_PRICE_SELECTOR).text).replace(",", "")
    return float(price)
