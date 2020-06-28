from selenium import webdriver
import urllib.parse as urlparse
from selenium.common.exceptions import JavascriptException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time
import json
import inspect

URL_search = "https://www.finam.ru/analysis/search/"
PARAMS_search = {
    'text': 'default',
    'searchid': 2162809
}
SELECTOR_first_in_search = "#ya-site-results > div > yass-div > table.l-page.l-page_layout_70-30.l-page_type_search > tbody > tr > td > yass-div.b-body-items > yass-ol > yass-li:nth-child(1) > yass-div > yass-h3 > a"
BROKEN_PAGE_MESSAGE = 'Информация не может быть предоставлена.'


def get_id_and_code_for_company_from_html(driver):
    html_source = driver.page_source
    id = re.findall(r'"id": [\d\w]+', html_source)[1]
    id = int(id.split(':')[1])
    code = re.findall(r'"code": "[^",]+",', html_source)[0]
    code = code.split(': "')[1][:-2]
    return id, code


def get_company_from_html(driver):
    try:
        html_source = driver.page_source
        main = re.findall(r'Finam\.IssuerProfile\.Main.issue = .+};', html_source)[0]
        main = main.replace('Finam.IssuerProfile.Main.issue = ', '')[:-1]
        main = re.sub(r', *}', '}', main)
        main_json = json.loads(main)
        quote = main_json['quote']

        company = {
            'id': quote['id'],
            'name': quote['title'],
            'code': quote['code'],
            'link_name': quote['fullUrl'].split('/')[1],
            'id_market': quote['market']['id']
        }
        if company is None:
            raise Exception("Company is None")

        return company
    except Exception as e:
        raise e


def find_company(name):
    driver = webdriver.Chrome()
    params = PARAMS_search.copy()
    params['text'] = name
    params = urlparse.urlencode(params)
    url = URL_search + "?" + params
    driver.get(url)
    driver.find_element_by_css_selector(SELECTOR_first_in_search).click()


def click_on_market_el_with_js(market_index, driver):
    script = f'document.getElementsByClassName("finam-ui-dropdown-list")[0].getElementsByTagName("a")[{market_index}].click()'
    driver.execute_script(script)


def click_on_company_el_with_js(company_index, driver):
    script = f'document.getElementsByClassName("finam-ui-dropdown-list")[1].getElementsByTagName("a")[{company_index}].click()'
    driver.execute_script(script)


def click_on_company_dropdown(driver):
    exec_with_retry(lambda: driver
                    .find_element_by_css_selector(
        "#issuer-profile-header > div.finam-ui-quote-selector-quote > div")
                    .click())


def send_company_name(name, driver):
    exec_with_retry(
        lambda: driver.find_element_by_xpath('// *[ @ id = "issuer-profile-header"] / div[2] / input').clear())
    exec_with_retry(
        lambda: driver.find_element_by_xpath('// *[ @ id = "issuer-profile-header"] / div[2] / input').send_keys(
            f"{name}\n"))


def exec_with_retry(function, delay=200):
    start = time.perf_counter()
    now = time.perf_counter()
    while now - start < delay:
        try:
            res = function()
            return res
        except Exception as e:
            # print('Retry execute:' + inspect.getsource(function))
            time.sleep(1)
            now = time.perf_counter()
            if now - start > delay:
                raise e


def get_not_visited_companies(market_id, driver, db):
    company_list = list(map(lambda el: el.text, exec_with_retry(lambda: driver
                                                                .find_elements_by_class_name("finam-ui-dropdown-list")[1]
                                                                .find_elements_by_tag_name("a"))))
    company_list.pop(0)
    company_list = set(company_list)

    query = db.companies.select() \
        .where(db.companies.c.id_market == market_id) \
        .where(db.companies.c.name.in_(list(company_list)))
    visited_companies = db.engine.execute(query)
    visited_companies = set(map(lambda row: row[1], visited_companies))

    return list(company_list - visited_companies)


def save_market(market, db):
    try:
        db.engine.execute(
            db.markets.insert().values(
                market
            )
        )
        print('Saved market to db: ' + str(market))
    except Exception as e:
        print('Do not save market to db: ' + str(market) + '\nBecause of ' + str(e.__cause__))


def save_company(company, db):
    try:
        db.engine.execute(
            db.companies.insert().values(
                company
            )
        )
        print('Saved company to db: ' + str(company))
    except Exception as e:
        print('Do not save company to db: ' + str(company) + '\nBecause of ' + str(e.__cause__))


def get_market_name(driver):
    return exec_with_retry(lambda: driver.find_element_by_xpath(
        '//*[@id="issuer-profile-header"]/div[1]/div[1]').text)


def fill_all_markets_and_companies(db):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.finam.ru/profile/moex-akcii/polymetal-international-plc/old/?market=200")
        exec_with_retry(lambda: driver.find_element_by_css_selector(
            "#issuer-profile-header > div.finam-ui-quote-selector-market > div.finam-ui-quote-selector-arrow").click())
        market_list = exec_with_retry(lambda: driver
                                      .find_elements_by_class_name("finam-ui-dropdown-list")[0]
                                      .find_elements_by_tag_name("a"))
        for index_market in range(len(market_list) - 1, 1, -1):
            start_index_company = 1
            while True:
                if not exec_with_retry(lambda: market_list[index_market].is_displayed()):
                    exec_with_retry(lambda: driver.find_element_by_css_selector(
                        "#issuer-profile-header > div.finam-ui-quote-selector-market > div.finam-ui-quote-selector-arrow") \
                                    .click())
                click_on_market_el_with_js(index_market, driver)

                click_on_company_dropdown(driver)
                company_list = list(
                    map(lambda el: el.text,
                        exec_with_retry(lambda: driver
                                        .find_elements_by_class_name("finam-ui-dropdown-list")[1]
                                        .find_elements_by_tag_name("a"))))
                if len(company_list) < start_index_company + 1:
                    break
                market_name = get_market_name(driver)
                send_company_name(company_list[start_index_company], driver)
                if BROKEN_PAGE_MESSAGE in driver.page_source or market_name != get_market_name(driver):
                    driver.back()
                    start_index_company += 1
                    market_list = exec_with_retry(lambda: driver
                                                  .find_elements_by_class_name("finam-ui-dropdown-list")[0]
                                                  .find_elements_by_tag_name("a"))
                    continue
                break

            if len(company_list) < start_index_company + 1:
                continue

            link_paths = driver.current_url.split('/')
            params_query = driver.current_url.split('?')[1]
            url_params = dict(urlparse.parse_qsl(params_query))

            market = {
                'id': url_params.get("market"),
                'link_name': link_paths[4],
                'name': get_market_name(driver)
            }
            save_market(market, db)

            company = exec_with_retry(lambda: get_company_from_html(driver), 30)
            save_company(company, db)

            click_on_company_dropdown(driver)
            company_list = get_not_visited_companies(market['id'], driver, db)

            for index_company in range(0, len(company_list)):
                send_company_name(company_list[index_company], driver)
                link_paths = driver.current_url.split('/')
                if market['link_name'] != link_paths[4] or BROKEN_PAGE_MESSAGE in driver.page_source:
                    driver.back()
                    continue

                company = exec_with_retry(lambda: get_company_from_html(driver), 30)
                save_company(company, db)

                if market['name'] != get_market_name(driver) and market['link_name'] == link_paths[4]:
                    driver.back()

            market_list = exec_with_retry(lambda: driver
                                          .find_elements_by_class_name("finam-ui-dropdown-list")[0]
                                          .find_elements_by_tag_name("a"))
    except Exception as e:
        print(f'Error of page: {driver.current_url}')
        driver.save_screenshot('../errorScreen.png')
        raise e
    finally:
        driver.close()
