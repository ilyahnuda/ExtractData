import datetime as datetime


class StockIndexObj:
    def __init__(self, symbol: str, date: datetime, open_val: float, high_val: float, low_val: float,
                 close_val: float, adj_close: float, volume_val: int):
        self.symbol = symbol
        self.date = date.date()
        self.open_val = round(open_val, 4)
        self.high_val = round(high_val, 4)
        self.low_val = round(low_val, 4)
        self.close_val = round(close_val, 4)
        self.adj_close = round(adj_close, 4)
        self.volume_val = volume_val
