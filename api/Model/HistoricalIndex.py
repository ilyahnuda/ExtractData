import sqlalchemy

from sqlalchemy import Integer, String, \
    Column, DateTime, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HistoricalDataIndex(Base):
    __tablename__ = 'stocks_historicaldataindex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    financeindex_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    open_val = Column(DECIMAL, nullable=False)
    high_val = Column(DECIMAL, nullable=False)
    low_val = Column(DECIMAL, nullable=False)
    close_val = Column(DECIMAL, nullable=False)
    adjclose_val = Column(DECIMAL, nullable=False)
    volume_val = Column(DECIMAL, nullable=False)
