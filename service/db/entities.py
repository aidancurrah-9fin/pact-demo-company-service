from sqlalchemy import String, ARRAY
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    street_name: Mapped[str] = mapped_column()
    regions: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])
