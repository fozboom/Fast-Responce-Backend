from sqlalchemy.orm import Mapped

from app.database import Base, int_pk, int_null_true


class Location(Base):
    id: Mapped[int_pk]
    city: Mapped[str]
    street: Mapped[str]
    house_number: Mapped[int]
    apartment_number: Mapped[int_null_true]
    latitude: Mapped[float]
    longitude: Mapped[float]

    extend_existing = True



