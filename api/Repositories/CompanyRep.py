from api.Database.Db import Database
from sqlalchemy.orm import Session

from api.Model.Company import Company


class CompanyRep:
    __db = None

    def __init__(self, db: Database):
        self.__db = db

    def add_company(self, company: Company):
        session = Session(bind=self.__db.get_engine())
        session.add(company)
        session.commit()

    def get_all(self):
        session = Session(bind=self.__db.get_engine())
        companies = session.query(Company).all()
        session.close()
        return companies

    def update_company(self, name, new_values: Company):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(Company).filter(Company.name == name).first()

        obj.symbol = new_values.symbol
        obj.price = new_values.price
        obj.weight = new_values.weight
        obj.chg = new_values.chg
        obj.percent_chg = new_values.percent_chg

        session.add(obj)
        session.commit()
        session.close()

    def delete_company(self, name):
        session = Session(bind=self.__db.get_engine())
        obj = session.query(Company).filter(Company.name == name).first()
        session.delete(obj)
        session.commit()
        session.close()

    def get_by_symbol(self, symbol: str):
        session = Session(bind=self.__db.get_engine())
        company = session.query(Company).filter(Company.symbol == symbol).all()
        session.close()
        return company[0].id

    def check_if_exist(self, name):
        session = Session(bind=self.__db.get_engine())
        exists = session.query(Company).filter(Company.name == name).first()
        session.close()
        return exists