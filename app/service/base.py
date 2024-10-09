from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.database import Session


class BaseService:
    model = None
    @classmethod
    async def find_all(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model)
            return await session.stream_scalars(query)

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with Session() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with Session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
