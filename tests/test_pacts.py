import os
import time
from multiprocessing import Process
from pathlib import Path
from typing import Generator, Literal, Any, Callable

import pytest
import uvicorn
from pact import Verifier
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from service.app import app
from service.db.entities import Company


def start_server():
    uvicorn.run(
        app,
        host="localhost",
        port=3333,
    )


@pytest.fixture
def test_server(mocked_environment: None) -> Generator[None, None, None]:
    proc = Process(target=start_server, args=())
    proc.start()
    time.sleep(1)

    yield

    proc.terminate()


def create_company(
    postgres_db_url: str,
) -> Callable[[Literal["setup", "teardown"], dict[str, Any] | None], None]:
    def wrapped(
        action: Literal["setup", "teardown"],
        parameters: dict[str, Any] | None,
    ) -> None:
        engine = create_engine(postgres_db_url)
        with Session(engine) as session:
            if action == "setup":
                base_company = Company(
                    id=1,
                    street_name="Test",
                    regions=["Europe"]
                )
                session.add(base_company)

            if action == "teardown":
                session.query(Company).delete()

            session.commit()

    return wrapped


def test_provider(
    postgres_database: str,
    test_server: None,
):
    state_handlers = {
        "Company ID 1 exists": create_company(postgres_database),
        "Company ID 2 does not exist": lambda action, parameters: None,
    }

    verifier = (
        Verifier("company-service")
        .add_transport(url="http://localhost:3333")
        .state_handler(state_handlers, teardown=True)
    )

    if "pact-broker-url" in os.environ:
        verifier.broker_source(
            os.environ["pact-broker-url"], token=os.environ["PACT_BROKER_TOKEN"]
        ).set_publish_options(
            version=os.environ["GIT_HEAD_REF"],
            branch="main",
        )
    else:
        verifier.add_source(Path(__file__).parent.parent / "pacts")

    verifier.verify()
