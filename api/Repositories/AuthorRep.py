from sqlalchemy.orm import Session

from api.Database.Db import Database
from api.Model.Author import Author


class AuthorRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_author(self, author: Author):
        session = Session(bind=self.__db.get_engine())
        session.add(author)
        session.commit()
        session.close()

    def get_all(self, name=None):
        session = Session(bind=self.__db.get_engine())
        if name:
            authors = session.query(Author).filter(Author.name == name).all()
        else:
            authors = session.query(Author).all()
        session.close()
        return authors

    def check_if_exist(self, name):
        session = Session(bind=self.__db.get_engine())
        exists = session.query(Author).filter(Author.name == name).first()
        session.close()
        return exists
