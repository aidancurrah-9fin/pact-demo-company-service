from service.models import Company, Region
from service.db.entities import Company as CompanyTable


class CompanyTransformer:
    @staticmethod
    def from_db(company_orm: CompanyTable) -> Company:
        return Company(
            id=company_orm.id,
            street_name=company_orm.street_name,
            regions=[Region(region) for region in company_orm.regions],
        )
