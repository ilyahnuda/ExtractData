import sqlalchemy

from sqlalchemy import Integer, String, \
    Column, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Author(Base):
    __tablename__ = 'stocks_author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
