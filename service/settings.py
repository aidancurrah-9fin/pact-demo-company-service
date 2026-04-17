from logging import getLogger, Logger

from pydantic import PostgresDsn, BaseModel, Field
from pydantic_settings import BaseSettings

from service.db.dbal import CompanyDBAL, CompanyDBALProtocol


class EnvironmentSettings(BaseSettings):
    db_url: PostgresDsn


class Settings(BaseModel):
    environment: EnvironmentSettings
    logger: Logger
    dbal: CompanyDBALProtocol

    class Config:
        arbitrary_types_allowed = True


def get_settings() -> Settings:
    logger = getLogger()
    env_settings = EnvironmentSettings()

    return Settings(
        environment=env_settings,
        logger=logger,
        dbal=CompanyDBAL(
            connection_url=env_settings.db_url,
            logger=logger,
        ),
    )
