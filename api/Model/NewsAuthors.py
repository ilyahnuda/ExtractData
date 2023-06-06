from sqlalchemy import Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NewsAuthors(Base):
    __tablename__ = 'stocks_news_authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, nullable=False)
    author_id = Column(Integer, nullable=False)
