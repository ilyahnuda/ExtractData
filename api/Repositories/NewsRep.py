from api.Database.Db import Database
from sqlalchemy.orm import Session

from api.Model.News import News


class NewsRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_news(self, news: News):
        session = Session(bind=self.__db.get_engine())
        session.add(news)
        session.commit()
        session.close()

    def get_all(self):
        session = Session(bind=self.__db.get_engine())
        news = session.query(News).all()
        session.close()
        return news

    def get_by(self, title=None):
        session = Session(bind=self.__db.get_engine())
        query = session.query(News)
        if title:
            query = query.filter(News.title == title)

        query = query.all()
        session.close()
        return query

    def update_news(self, title, news: News):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(News).filter(News.title == title).first()

        obj.text = news.text
        obj.img = news.img

        session.add(obj)
        session.commit()
        session.close()

    def delete_news(self, title):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(News).filter(News.title == title).first()

        session.delete(obj)
        session.commit()
        session.close()

    def check_if_exist(self, title):
        session = Session(bind=self.__db.get_engine())
        exists = session.query(News).filter(News.title == title).first()
        session.close()
        return exists
