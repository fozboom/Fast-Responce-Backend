from datetime import datetime
from typing import Annotated

from sqlalchemy import func, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from contextlib import asynccontextmanager
from app.config import get_db_url

DATABASE_URL = get_db_url()

# Asynchronous engine for working with the database
engine = create_async_engine(DATABASE_URL)
# Factory of sessions for working with the database
Session = async_sessionmaker(engine, expire_on_commit=False)


str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
int_null_true = Annotated[int, mapped_column(nullable=True)]


# Base class for all models
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"



def connection(method):
    async def wrapper(*args, **kwargs):
        async with Session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper