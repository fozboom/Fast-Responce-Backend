from sqlalchemy.orm import Mapped, relationship
from app.database import str_uniq, int_pk
from app.database import Base


class Role(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    users = relationship("User", back_populates="role")

    extend_existing = True  # For update existing table, if table already exists


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
