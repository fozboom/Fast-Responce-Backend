from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from enum import Enum
from datetime import date

from app.sql_enums import GenderEnum


class Patient(Base):
    name: Mapped[str]
    birth_date: Mapped[date]
    gender: Mapped[GenderEnum]
    phone: Mapped[str | None]
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    location = relationship("Location", back_populates="patients", lazy="joined")
    calls = relationship("Call", back_populates="patient")
