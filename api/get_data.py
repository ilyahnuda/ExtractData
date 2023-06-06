import datetime
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from yahoo_fin.stock_info import get_data
from selenium.webdriver.common.keys import Keys
from dateutil.parser import parse
from api.APIConfig import Config
from api.Objects.Company import CompanyObj
from api.Objects.HistoricalIndex import HistoricalIndexObj
from api.Objects.News import NewsObj
from api.Objects.StockIndex import StockIndexObj
from api.ScrapUtils import ScrapUtils
from selenium.webdriver.chrome.options import Options


class APIStock:

    def __init__(self, config: Config):
        self.cfg = config

    def get_html_file(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_data_from_wiki(self):
        url = self.cfg.API_URL_WIKI
        body = self.get_html_file(url)
        table_body = body.find('tbody')
        rows = table_body.find_all('tr')
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    def get_preprocess_wiki_data(self):
        result = dict()
        data = self.get_data_from_wiki()
        for company in data:
            result[company[0]] = [company[2], company[3], re.findall("\d{4}", company[-1])[0]]
        return result

    def get_data_from_slickcharts(self):
        url = self.cfg.API_SLICK_WIKI
        driver = create_chrome_driver()
        driver.get(url)
        table = driver.find_element(by=By.TAG_NAME, value='tbody')
        data = []
        wiki_data = self.get_preprocess_wiki_data()
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        for row in rows:
            cols = row.find_elements(by=By.TAG_NAME, value='td')
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        return transform_to_company_obj(companies=data, wiki_data=wiki_data)

    def get_historical_data(self, names: list, interval='1d'):
        for name in names:
            data = get_data(name, datetime.date.today() - datetime.timedelta(days=365 * 5), index_as_date=True,
                            interval=interval)
            objects = transform_to_stock_obj(data)
            yield objects

    def get_SP500_historical(self, interval='1d'):
        data = get_data("^GSPC", datetime.date.today() - datetime.timedelta(days=365 * 5), index_as_date=True,
                        interval=interval)
        objects = transform_to_hist_index_obj(data)
        return objects

    def get_finance_news_reuters(self):
        urls = []
        url = self.cfg.URL_REUTERS_NEWS
        driver = create_chrome_driver()
        driver.get(url)
        ScrapUtils.clicks(driver)
        body = driver.find_elements(by='class name', value='content-layout__item__SC_GG')
        for content in body[1:]:
            elements = content.find_elements(by='tag name', value='li')
            for item in elements:
                url = item.find_elements(by='tag name', value='a')[1].get_attribute('href')
                urls.append(url)
        driver.close()
        return urls

    # доработать
    def get_finance_content_reuters(self, urls: list):
        news = []
        driver = create_chrome_driver()
        for url in urls:
            driver.get(url)
            ScrapUtils.accept_cookie(driver)
            try:
                title = driver.find_element(by="class name", value="article-header__heading__15OpQ").find_element(
                    by="tag name", value="h1").text
            except:
                break
            author = [x.text for x in
                      driver.find_element(by="class name", value="article-header__heading__15OpQ").find_elements(
                          by='tag name', value='a')]
            all_author = ''
            for auth in author:
                all_author = all_author + auth + ' '
            time_news = [x.text for x in driver.find_elements(by="class name", value="date-line__date__23Ge-")[1:3]]
            time_news = time_news[0] + ' ' + time_news[1]
            try:
                img = driver.find_element(by="xpath",
                                          value="//div[@data-testid='Image']").find_element(
                    by="tag name",
                    value="img").get_attribute('src')
            except:
                continue
            try:
                img_description = driver.find_element(by="xpath",
                                                      value="//figcaption[@data-testid='Body']").text

            except:
                try:
                    img_description = driver.find_element(by="xpath",
                                                          value="//p[@data-testid='Body']").text
                except:
                    img_description = driver.find_element(by="xpath",
                                                          value="//p[@data-testid='Text']").text

            body = [x.text for x in driver.find_elements(by="tag name", value="p")]
            total_body = ''
            for string in body:
                total_body = total_body + string + '\n'
            news.append(
                transform_to_news_obj(title=title, author=all_author, time=time_news,
                                      img_description=img_description,
                                      img=img, body=total_body, link=None))
            time.sleep(2)
        driver.close()

        return news

    def get_finance_news_urls_yahoo(self):
        url = self.cfg.API_YAHOO_FINANCE_NEWS
        driver = create_chrome_driver()
        driver.get(url)
        ScrapUtils.scroll_max(driver)
        result = driver.find_element(by="id", value="Fin-Stream-Proxy")
        result = result.find_elements(by="tag name", value="li")

        news_urls = []
        for item in result:
            news_url = item.find_element(by="tag name", value="a")
            href = news_url.get_attribute('href')
            if 'beap.gemini.yahoo.com' in href or 'legal.yahoo.com/us/en/yahoo' in href:
                continue
            news_urls.append(href)

        driver.close()
        return news_urls

    # +
    def get_content_finance_news_yahoo(self, urls: list):
        news = []
        driver = create_chrome_driver()
        for url in urls:
            print(url)
            driver.get(url)
            title = driver.find_element(by="class name", value="caas-title-wrapper").find_element(by="tag name",
                                                                                                  value="h1").text
            author = driver.find_element(by="class name", value="caas-author-byline-collapse").text.lower().split(
                ' and ')
            time_news = driver.find_element(by="class name", value="caas-attr-time-style").find_element(by="tag name",
                                                                                                        value="time").text
            try:
                url_more = driver.find_element(by="class name", value="caas-readmore").find_element(by="tag name",
                                                                                                    value="a")
                url_more = url_more.get_attribute('href')
            except:
                print(f"url_err: {url}")
                url_more = None
            try:
                img = driver.find_element(by="class name", value="caas-img-container").find_element(by="tag name",
                                                                                                    value="img").get_attribute(
                    'src')
                if len(img) > 200:
                    raise Exception
            except:
                print(f"err: {url}")
                img = None
            try:
                img_description = driver.find_element(by="tag name", value="figcaption").text
            except Exception as e:
                img_description = None

            body = driver.find_element(by="class name", value="caas-body").text

            news.append(
                transform_to_news_obj(title=title, author=author, time=parse(time_news), img_description=img_description,
                                      img=img, body=body, link=url_more))
        driver.close()
        return news

    def get_names(self):
        name_data = self.get_data_from_wiki()
        names = [x[0].replace('.', '-') for x in name_data]
        return names


def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver


def transform_to_stock_obj(data: pd.DataFrame):
    all_rows = []
    for index, row in data.iterrows():
        obj = StockIndexObj(symbol=row[6], date=index.to_pydatetime(), open_val=row[0], high_val=row[1], low_val=row[2],
                            close_val=row[3], adj_close=row[4], volume_val=row[5])
        all_rows.append(obj)
    return all_rows


def transform_to_company_obj(companies: list, wiki_data):
    obj_companies = []
    for company in companies:
        company_info = wiki_data[company[2]]
        weight = float(company[3].replace(',', ''))
        price = float(company[4].replace(',', ''))
        chg = float(company[5].replace(',', ''))
        symbol = company[2].replace('.', '-')
        obj = CompanyObj(name=company[1], symbol=symbol, weight=weight, price=price,
                         chg=chg, percent_chg=float(re.findall('-?\d+.\d+', company[6])[0]),
                         founded=company_info[2],
                         sector=company_info[0], sub_sector=company_info[1])
        obj_companies.append(obj)
    return obj_companies


def transform_to_news_obj(**kwargs):
    return NewsObj(title=kwargs['title'], author=kwargs['author'], time=kwargs['time'], img=kwargs['img'],
                   img_description=kwargs['img_description'], body=kwargs['body'], link=kwargs['link'])


def transform_to_hist_index_obj(data: pd.DataFrame):
    all_rows = []
    for index, row in data.iterrows():
        obj = HistoricalIndexObj(symbol=row[6], date=index.to_pydatetime(), open_val=row[0], high_val=row[1],
                                 low_val=row[2],
                                 close_val=row[3], adj_close=row[4], volume_val=row[5])
        all_rows.append(obj)
    return all_rows


if __name__ == '__main__':
    str_date = 'Thu, May 18, 2023 at 3:37 PM GMT+3'
    date = parse(str_date)
    print(date)
    print(type(date))
