from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from service.db.entities import Company


@pytest.fixture(scope="module")
def seed_data(postgres_database: str) -> Generator[None, None, None]:
    engine = create_engine(postgres_database)
    with Session(engine) as session:
        base_company = Company(
            id=1,
            street_name="Test",
            regions=["Europe"]
        )
        session.add(base_company)
        session.commit()

    yield

    with Session(engine) as session:
        session.query(Company).delete()
        session.commit()


@pytest.mark.parametrize(
    "company_id, status, expected",
    [
        (1, 200, {"id": 1, "street_name": "Test", "regions": ["Europe"]}),
        (2, 404, {"detail": "Company not found"}),
    ],
)
def test_get_company(
    company_id: int,
    status: int,
    expected: dict,
    test_app: TestClient,
    seed_data: None
) -> None:
    response = test_app.get(f"/{company_id}")

    assert response.status_code == status
    assert response.json() == expected
