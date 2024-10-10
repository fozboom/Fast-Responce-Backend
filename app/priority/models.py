from sqlalchemy.orm import Mapped, declared_attr

from app.database import Base, int_pk, str_uniq

class Priority(Base):
    __tablename__ = "priorities"
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str]
    level : Mapped[int]

    extend_existing = True



    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})(name={self.name})(level={self.level})"