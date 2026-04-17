import os
from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from service.db.entities import Company, Base
from service.app import app


@fixture(scope="session")
def postgres_database() -> Generator[str, None, None]:
    with PostgresContainer("postgres:16", dbname="postgres") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)

        yield postgres.get_connection_url()


@fixture(scope="session")
def mocked_environment(
    postgres_database: str,
) -> None:
    os.environ["DB_URL"] = postgres_database


@fixture
def test_app(mocked_environment: None) -> TestClient:
    return TestClient(app)
