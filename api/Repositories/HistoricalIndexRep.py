from sqlalchemy.orm import Session
from sqlalchemy import desc
from api.Database.Db import Database
from api.Model.HistoricalIndex import HistoricalDataIndex


class HistoricalDataIndexRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_stock_index(self, instance: HistoricalDataIndex):
        session = Session(bind=self.__db.get_engine())
        session.add(instance)
        session.commit()
        session.close()

    def get_stock_index(self, fin_id=None, datetime_begin=None, datetime_end=None):
        session = Session(bind=self.__db.get_engine())
        query = session.query(HistoricalDataIndex)
        if fin_id:
            query = query.filter(HistoricalDataIndex.financeindex_id_id == fin_id)
        if datetime_begin:
            query = query.filter(HistoricalDataIndex.date >= datetime_begin)
        if datetime_end:
            query = query.filter(HistoricalDataIndex.date <= datetime_end)

        instances = query.all()
        session.close()
        return instances

    def check_if_exist_row(self, date, index_id):
        session = Session(bind=self.__db.get_engine())

        exists = session.query(HistoricalDataIndex).filter(HistoricalDataIndex.date == date,
                                                           HistoricalDataIndex.financeindex_id == index_id).first()

        session.close()
        return exists

    def order_data_by_date(self):
        session = Session(bind=self.__db.get_engine())
        instance = session.query(HistoricalDataIndex).order_by(desc(HistoricalDataIndex.date)).first()
        session.close()
        return instance
