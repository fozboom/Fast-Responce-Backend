from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk
from enum import Enum
from datetime import date

class Gender(str, Enum):
    male = "male"
    female = "female"


class Patient(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    birth_date: Mapped[date]
    gender: Mapped[str]
    phone: Mapped[str]
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    location = relationship("Location", back_populates="patients")
