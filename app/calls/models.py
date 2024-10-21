from app.database import str_uniq
from sqlalchemy import String, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text
from app.sql_enums import StatusEnum, PriorityEnum


class Call(Base):
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"))

    driver_name: Mapped[str | None]
    operator_name: Mapped[str | None]
    doctor_name: Mapped[str | None]

    diagnosis: Mapped[str | None]
    description: Mapped[str | None]

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    priority: Mapped[PriorityEnum] = mapped_column(default=PriorityEnum.HIGH, server_default=text("HIGH"))

    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.REQUEST_CREATED,
                                               server_default=text("'REQUEST_CREATED'"))

    patient = relationship(
        "Patient",
        back_populates="calls",
        lazy="joined"
    )

    location = relationship(
        "Location",
        back_populates="calls",
        lazy="joined"
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
