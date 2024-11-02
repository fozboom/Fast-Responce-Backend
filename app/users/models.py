from sqlalchemy.orm import Mapped
from app.database import str_uniq

from app.database import Base
from app.sql_enums import RoleEnum, GenderEnum
from datetime import date


class User(Base):
    username: Mapped[str_uniq]
    full_name: Mapped[str]
    hashed_password: Mapped[str]
    role: Mapped[RoleEnum]
    gender: Mapped[GenderEnum]
    email: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]
    birth_date: Mapped[date]
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
