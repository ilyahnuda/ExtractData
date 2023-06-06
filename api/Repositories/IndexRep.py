from sqlalchemy.orm import Session

from api.Database.Db import Database
from api.Model.Index import Index


class IndexRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_index(self, index: Index):
        session = Session(bind=self.__db.get_engine())
        session.add(index)
        session.commit()
        session.close()

    def get_all(self, name=None):
        session = Session(bind=self.__db.get_engine())
        if name:
            indexes = session.query(Index).filter(Index.name == name).all()
        else:
            indexes = session.query(Index).all()
        session.close()
        return indexes

    def check_if_exist(self, name):
        session = Session(bind=self.__db.get_engine())
        exists = session.query(Index).filter(Index.name == name).first()
        session.close()
        return exists
