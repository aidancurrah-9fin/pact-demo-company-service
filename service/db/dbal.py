from logging import Logger
from typing import Protocol, runtime_checkable

from pydantic import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from service.db.transformers import CompanyTransformer
from service.models import Company
from service.db.entities import Company as CompanyTable


@runtime_checkable
class CompanyDBALProtocol(Protocol):
    def get_company(self, company_id: int) -> Company:
        pass


class CompanyDBAL(CompanyDBALProtocol):
    def __init__(self, connection_url: PostgresDsn, logger: Logger) -> None:
        engine = create_engine(str(connection_url))

        self.session = Session(bind=engine)
        self.logger = logger

    def get_company(self, company_id: int) -> Company | None:
        company = self.session.get(CompanyTable, company_id)
        if company is None:
            return None
        return CompanyTransformer.from_db(company)
