from sqlalchemy import desc

from api.Database.Db import Database
from api.Model.StockIndex import StockIndex
from sqlalchemy.orm import Session


class StockRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_stock_index(self, instance: StockIndex):
        session = Session(bind=self.__db.get_engine())
        session.add(instance)
        session.commit()
        session.close()

    def get_stock_index(self, name=None, datetime_begin=None, datetime_end=None):
        session = Session(bind=self.__db.get_engine())
        query = session.query(StockIndex)
        if name:
            query = query.filter(StockIndex.symbol == name)
        if datetime_begin:
            query = query.filter(StockIndex.date >= datetime_begin)
        if datetime_end:
            query = query.filter(StockIndex.date <= datetime_end)

        instances = query.all()
        session.close()
        return instances

    def update_stock_index(self, name, new_instance: StockIndex):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(StockIndex).filter(StockIndex.symbol == name).first()
        obj.date = new_instance.date
        obj.open_val = new_instance.open_val
        obj.low_val = new_instance.low_val
        obj.adjclose_val = new_instance.adjclose_val
        obj.close_val = new_instance.close_val
        obj.high_val = new_instance.high_val
        obj.volume_val = new_instance.volume_val
        session.add(obj)
        session.commit()
        session.close()

    def delete_stock_index(self, name):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(StockIndex).filter(StockIndex.symbol == name).first()
        session.delete(obj)
        session.commit()
        session.close()

    def order_data_by_date(self):
        session = Session(bind=self.__db.get_engine())
        instance = session.query(StockIndex).order_by(desc(StockIndex.date)).first()
        session.close()
        return instance