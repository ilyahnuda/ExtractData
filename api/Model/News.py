from datetime import datetime

from sqlalchemy import Integer, String, \
    Column, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = "stocks_news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    time = Column(DateTime, nullable=False, default=datetime.now)
    img = Column(String(300), nullable=True)
    img_description = Column(String(500), nullable=True)
    text = Column(Text)
    link = Column(String(200), nullable=True)
