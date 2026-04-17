from fastapi import FastAPI, HTTPException

from service.models import Company
from service.settings import get_settings

app = FastAPI()


@app.get("/{company_id}")
def get_company_by_id(company_id: int) -> Company:
    settings = get_settings()
    settings.logger.info(f"Request for {company_id=}")

    company = settings.dbal.get_company(company_id=company_id)

    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return company
