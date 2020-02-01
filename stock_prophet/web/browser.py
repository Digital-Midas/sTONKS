from selenium import webdriver
import urllib.parse as urlparse

URL_search = "https://www.finam.ru/analysis/search/"
PARAMS_search = {
    'text': 'default',
    'searchid': 2162809
}
SELECTOR_first_in_search = "#ya-site-results > div > yass-div > table.l-page.l-page_layout_70-30.l-page_type_search > tbody > tr > td > yass-div.b-body-items > yass-ol > yass-li:nth-child(1) > yass-div > yass-h3 > a"

def find_company(name):
    driver = webdriver.Chrome()
    params = PARAMS_search.copy()
    params['text'] = name
    params = urlparse.urlencode(params)
    url = URL_search + "?" + params
    driver.get(url)
    driver.find_element_by_css_selector(SELECTOR_first_in_search).click()


def fill_all_markets_and_companies():
    driver = webdriver.Chrome()
    driver.get("https://www.finam.ru/profile/moex-akcii/polymetal-international-plc/?market=200")
    driver.find_element_by_css_selector("#issuer-profile-header > div.finam-ui-quote-selector-market > div.finam-ui-quote-selector-arrow").click()
    market_list = driver.find_element_by_xpath("/html/body/div[15]/div/ul").find_elements_by_tag_name("li")
    for index_market in range(0, len(market_list)):
        if not market_list[index_market].is_displayed():
            driver.find_element_by_css_selector(
                "#issuer-profile-header > div.finam-ui-quote-selector-market > div.finam-ui-quote-selector-arrow").click()
        market_list[index_market].click()
        driver.find_element_by_css_selector("#issuer-profile-header > div.finam-ui-quote-selector-quote > div").click()
        company_list = driver.find_element_by_xpath("/html/body/div[16]/div/ul").find_elements_by_tag_name("li")

        names_list = []
        for el in company_list:
            names_list.append(el.find_element_by_tag_name("a").text)

        print(names_list)

        for index_company in range(1, len(company_list)):
            print(str(index_company) + ": " + names_list[index_company])

            driver.find_elements_by_tag_name("input")[0].clear()
            driver.find_elements_by_tag_name("input")[0].send_keys(names_list[index_company] + "\n")

        market_list = driver.find_element_by_xpath("/html/body/div[15]/div/ul").find_elements_by_tag_name("li")

    driver.close()