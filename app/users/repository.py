from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.base_repository import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository):
    model = User

    # @classmethod
    # async def update_refresh_token(cls, session: AsyncSession, username: str, refresh_token: str):
    #     stmt = cls.model.update().where(cls.model.username == username).values(refresh_token=refresh_token)
    #     await session.execute(stmt)
    #     try:
    #         await session.commit()
    #     except SQLAlchemyError as e:
    #         await session.rollback()
    #         raise e
    #     return refresh_token
