import math

from api.APIConfig import DBConfig, Config
from api.Database.Db import Database
from api.Model.Author import Author
from api.Model.Company import Company
from api.Model.HistoricalIndex import HistoricalDataIndex
from api.Model.Index import Index
from api.Model.News import News
from api.Model.NewsAuthors import NewsAuthors
from api.Model.StockIndex import StockIndex

from api.Repositories.AuthorRep import AuthorRep
from api.Repositories.CompanyRep import CompanyRep
from api.Repositories.HistoricalIndexRep import HistoricalDataIndexRep
from api.Repositories.IndexRep import IndexRep
from api.Repositories.NewsAuthorRep import NewsAuthorsRep
from api.Repositories.NewsRep import NewsRep
from api.Repositories.StockRep import StockRep
from api.get_data import APIStock


# def fill_authors(self, authors, all_authors=[]):
#     for author in authors:
#         if author not in all_authors:
#             all_authors.append(author)
#             author = Author(name=author)
#             self.__authorRep.add_author(author)

class FillDB:
    __companyRep = None
    __newsRep = None
    __stockRep = None
    __indexRep = None
    __histIndexRep = None
    __authorRep = None
    __newsAuthorRep = None

    def __init__(self, companyRep: CompanyRep, newsRep: NewsRep, stockRep: StockRep, indexRep: IndexRep,
                 histIndexRep: HistoricalDataIndexRep, authorRep: AuthorRep, newsAuthorRep: NewsAuthorsRep,
                 api: APIStock):
        self.__companyRep = companyRep
        self.__stockRep = stockRep
        self.__newsRep = newsRep
        self.__indexRep = indexRep
        self.__histIndexRep = histIndexRep
        self.__authorRep = authorRep
        self.__newsAuthorRep = newsAuthorRep
        self.__api = api

    def fill_news(self, data):
        for obj in data:
            authors = obj.author
            self.fill_authors(authors)
            if not self.__newsRep.check_if_exist(obj.title):
                news = News(title=obj.title, img_description=obj.img_description,
                            img=obj.img, text=obj.body, time=obj.time, link=obj.link)
                self.__newsRep.add_news(news)
                self.fill_newsauthor(obj, authors)

    def fill_authors(self, authors):
        for author in authors:
            if not self.__authorRep.check_if_exist(name=author):
                author = Author(name=author)
                self.__authorRep.add_author(author)

    def fill_newsauthor(self, news, authors):
        news_id = self.__newsRep.get_by(news.title)[0].id
        for author in authors:
            author_id = self.__authorRep.get_all(author)[0].id
            if not self.__newsAuthorRep.check_if_exist(news_id=news_id, author_id=author_id):
                inst = NewsAuthors(news_id=news_id, author_id=author_id)
                self.__newsAuthorRep.add_newsauthors(inst)

    def fill_companies(self, data):
        for obj in data:
            company = Company(name=obj.name, symbol=obj.symbol, weight=obj.weight,
                              price=obj.price, chg=obj.chg, percent_chg=obj.percent_chg, founded=obj.founded,
                              sector=obj.sector, sub_sector=obj.sub_sector)
            if not self.__companyRep.check_if_exist(obj.name):
                self.__companyRep.add_company(company)
            else:
                self.__companyRep.update_company(company.name, company)

    def fill_stock_indexes(self, data: list):
        symbol = data[0].symbol
        symbol_id = self.__companyRep.get_by_symbol(symbol=symbol)
        last_date = self.__stockRep.order_data_by_date().date
        data = [obj for obj in data if obj.date > last_date]
        for obj in data:
            if math.isnan(obj.open_val):
                continue
            stock_index = StockIndex(symbol_id=symbol_id, date=obj.date, open_val=obj.open_val,
                                     high_val=obj.high_val, low_val=obj.low_val, close_val=obj.close_val,
                                     adjclose_val=obj.adj_close, volume_val=obj.volume_val)
            self.__stockRep.add_stock_index(stock_index)

    def fill_all_companies(self):
        objects = self.__api.get_data_from_slickcharts()
        self.fill_companies(objects)

    def fill_all_stocks(self):
        names = self.__api.get_names()
        for stock_company in self.__api.get_historical_data(names):
            self.fill_stock_indexes(stock_company)

    def fill_all_news(self):
        print("Start Yahoo")
        urls = self.__api.get_finance_news_urls_yahoo()
        news = self.__api.get_content_finance_news_yahoo(urls)
        self.fill_news(news)
        print("End Yahoo")
        print("Start reuters")
        # urls = self.__api.get_finance_news_reuters()
        print("Get urls")
        # news = self.__api.get_finance_content_reuters(urls)
        # self.fill_news(news)
        print("End reutors")

    # Вся аналитическые данные и сами название индексов две функции ниже
    def fill_all_indexes(self):
        if not self.__indexRep.check_if_exist(name='S&P500'):
            self.__indexRep.add_index(Index(name="S&P500"))
        objects = self.__api.get_SP500_historical()
        self.fill_hist_stock_index(objects)

    def fill_hist_stock_index(self, objects):
        index_name = objects[0].symbol
        if index_name == '^GSPC':
            index_name = 'S&P500'
        index_id = self.__indexRep.get_all(name=index_name)[0].id
        last_date = self.__histIndexRep.order_data_by_date().date
        objects = [obj for obj in objects if obj.date > last_date]
        for obj in objects:
            if math.isnan(obj.open_val):
                continue
            instance = HistoricalDataIndex(financeindex_id=index_id, date=obj.date, open_val=obj.open_val,
                                           high_val=obj.high_val, low_val=obj.low_val, close_val=obj.close_val,
                                           adjclose_val=obj.adj_close, volume_val=obj.volume_val)
            self.__histIndexRep.add_stock_index(instance)


def main():
    cfg = Config()
    db_cfg = DBConfig()

    db = Database(db_cfg)

    company_rep = CompanyRep(db)
    news_rep = NewsRep(db)
    stock_rep = StockRep(db)
    index_rep = IndexRep(db)
    hist_index = HistoricalDataIndexRep(db)
    author_rep = AuthorRep(db)
    newsauthor_rep = NewsAuthorsRep(db)

    api = APIStock(cfg)

    fill_db = FillDB(companyRep=company_rep, newsRep=news_rep, stockRep=stock_rep, indexRep=index_rep,
                     histIndexRep=hist_index, newsAuthorRep=newsauthor_rep, authorRep=author_rep, api=api)

    print("Start")
    fill_db.fill_all_companies()
    print("All companies")
    fill_db.fill_all_indexes()
    print("All indexes")
    fill_db.fill_all_stocks()
    print("All stocks")
    fill_db.fill_all_news()
    print("End")


if __name__ == '__main__':
    main()
