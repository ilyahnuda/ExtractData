class Config:

    def __init__(self):
        self.API_ENG_WIKI = 'https://en.wikipedia.org/wiki/'
        self.API_URL_WIKI = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        self.API_SLICK_WIKI = 'https://www.slickcharts.com/sp500'
        self.API_YAHOO_FINANCE = 'https://finance.yahoo.com/quote/{name}/history?period1={begin}&period2={' \
                                 'end}&interval={interval}&filter={filter}&frequency={' \
                                 'frequency}&includeAdjustedClose={includeAdjustedClose} '
        self.API_YAHOO_FINANCE_NEWS = 'https://finance.yahoo.com/topic/stock-market-news'
        self.URL_REUTERS_NEWS = 'https://www.reuters.com/business/finance/'
        self.Query_Param = QueryConfig()

    def construct_query_yahoo(self, name) -> str:
        qr = self.Query_Param
        return self.API_YAHOO_FINANCE.format(name=name, begin=qr.begin, end=qr.end, interval=qr.interval,
                                             filter=qr.filter, frequency=qr.frequency,
                                             includeAdjustedClose=qr.includeAdjustedClose)


class QueryConfig:
    def __init__(self):
        self.begin = '1453593600'
        self.end = '1674518400'
        self.interval = '1d'
        self.filter = 'history'
        self.frequency = '1d'
        self.includeAdjustedClose = True


class DBConfig:
    def __init__(self):
        self.driver = 'psycopg2'
        self.dialect = 'postgresql'
        self.username = 'postgres'
        self.password = '123456'
        self.host = 'localhost'
        self.port = '5432'
        self.db = 'MarketDB'
