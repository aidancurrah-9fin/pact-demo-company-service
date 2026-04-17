from enum import StrEnum

from pydantic import BaseModel


class Region(StrEnum):
    EUROPE = "Europe"
    NORTH_AMERICA = "North America"
    LATAM = "LATAM"


class Company(BaseModel):
    id: int
    street_name: str
    regions: list[Region]
