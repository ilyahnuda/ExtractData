from sqlalchemy.orm import Session

from api.Database.Db import Database
from api.Model.NewsAuthors import NewsAuthors


class NewsAuthorsRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_newsauthors(self, obj: NewsAuthors):
        session = Session(bind=self.__db.get_engine())
        session.add(obj)
        session.commit()
        session.close()

    def get_all(self):
        session = Session(bind=self.__db.get_engine())
        news_authors = session.query(NewsAuthors).all()
        session.close()
        return news_authors

    def check_if_exist(self, news_id, author_id):
        session = Session(bind=self.__db.get_engine())
        exists = session.query(NewsAuthors).filter(NewsAuthors.news_id == news_id,
                                                   NewsAuthors.author_id == author_id).first()
        session.close()
        return exists
