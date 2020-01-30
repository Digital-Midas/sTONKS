import requests
from bs4 import BeautifulSoup
import urllib.request as urlreq
import urllib.parse as urlparse

URL_for_company_search = "https://www.google.com/search"
PARAMS_search = {'q': 'default'}
SELECTOR_search_first = "#rso > div > div > div:nth-child(1) > div > div.rc > div.r > a"
URL_for_current = "https://markets.businessinsider.com/"
SELECTOR_current_price = "#site > div > div:nth-child(2) > div.row.equalheights.greyBorder > div > div:nth-child(3) > div.col-sm-10.no-padding > div.col-xs-12.no-padding > div:nth-child(2) > span"
URL_for_quotes = "http://export.finam.ru/quotes.txt"
PARAMS_quotes = {
    'market': 1,
    'em': 175924,
    'code': 'POLY',
    'cn': 'POLY',
    'apply': 0,
    'df': 1,
    'mf': 0,
    'yf': 2000,
    'dt': 2,
    'mt': 0,
    'yt': 2020,
    'p': 8,
    'e': '.txt',
    'dtf': 4,
    'tmf': 3,
    'MSOR': 1,
    'mstime': 'on',
    'mstimever': 1,
    'sep': 1,
    'sep2': 1,
    'datf': 1,
    'at': 1,
}
proxies = {
    "http": "95.79.99.148:3128"
}

"""
market - id биржи
em - id фирмы
code – текстовое id фирмы
df, mf, yf, from, dt, mt, yt, to – это параметры времени.
p — период котировок (тики, 1 мин., 5 мин., 10 мин., 15 мин., 30 мин., 1 час, 1 день, 1 неделя, 1 месяц)
e – расширение получаемого файла; возможны варианты — .txt либо .csv
dtf — формат даты (1 — ггггммдд, 2 — ггммдд, 3 — ддммгг, 4 — дд/мм/гг, 5 — мм/дд/гг)
tmf — формат времени (1 — ччммсс, 2 — ччмм, 3 — чч: мм: сс, 4 — чч: мм)
MSOR — выдавать время (0 — начала свечи, 1 — окончания свечи)
mstimever — выдавать время (НЕ московское — mstimever=0; московское — mstime='on', mstimever='1')
sep — параметр разделитель полей (1 — запятая (,), 2 — точка (.), 3 — точка с запятой (;), 4 — табуляция (»), 5 — пробел ( ))
sep2 — параметр разделитель разрядов (1 — нет, 2 — точка (.), 3 — запятая (,), 4 — пробел ( ), 5 — кавычка ('))
datf — Перечень получаемых данных (#1 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #2 — TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE; #3 — TICKER, PER, DATE, TIME, CLOSE, VOL; #4 — TICKER, PER, DATE, TIME, CLOSE; #5 — DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL; #6 — DATE, TIME, LAST, VOL, ID, OPER).
at — добавлять заголовок в файл (0 — нет, 1 — да)
"""


def get_quotes(company_id, date_from, date_to):
    params = urlparse.urlencode(PARAMS_quotes)
    response = urlreq.urlopen(URL_for_quotes + "?" + params)
    print(URL_for_quotes + "?" + params)
    return response


def get_current_stock_price(company_id):
    url = URL_for_current + "stocks/" + company_id + "-stock"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    price = str(soup.select_one(SELECTOR_current_price).text).replace(",", "")
    return float(price)


def find_company(name):
    params = PARAMS_search.copy()
    params['q'] = "finam" + name
    search_response = requests.get(URL_for_company_search, params=params, proxies=proxies)
    print(search_response.text)

    soup = BeautifulSoup(search_response.text, "lxml")
    link = soup.select_one(SELECTOR_search_first)
    return link


"""
http://export.finam.ru/quotes?
market=1&
em=175924&
code=POLY&
cn=POLY&
apply=0&
df=1&
mf=0&
yf=2000&
dt=1&
mt=0&
yt=2020&
p=8&
e=.txt&
dtf=4&
tmf=3&
MSOR=1&
mstime=on&
mstimever=1&
sep=1&
sep2=1&
datf=1&
at=1
"""
