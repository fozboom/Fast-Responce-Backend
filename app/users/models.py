from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import str_uniq, int_pk
from sqlalchemy import String, Boolean, ForeignKey
from app.database import Base


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }


