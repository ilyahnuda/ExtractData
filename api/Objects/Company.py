class CompanyObj:

    def __init__(self, name: str, symbol: str, weight: float, price: float, chg: float,
                 percent_chg: float, founded: int, sector: str, sub_sector: str):
        self.name = name
        self.symbol = symbol
        self.weight = weight
        self.price = price
        self.chg = chg
        self.percent_chg = percent_chg
        self.founded = founded
        self.sector = sector
        self.sub_sector = sub_sector
