from sqlalchemy.orm import Mapped, relationship

from app.database import Base, int_pk, int_null_true


class Location(Base):
    id: Mapped[int_pk]
    city: Mapped[str]
    street: Mapped[str]
    house_number: Mapped[int]
    apartment_number: Mapped[int_null_true]
    latitude: Mapped[float]
    longitude: Mapped[float]
    patients = relationship("Patient", back_populates="location")
    extend_existing = True

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "street": self.street,
            "house_number": self.house_number,
            "apartment_number": self.apartment_number,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


