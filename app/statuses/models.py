from sqlalchemy.orm import Mapped

from app.database import Base, int_pk, str_uniq


class Status(Base):
    __tablename__ = 'statuses'

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]
    extend_existing = True
