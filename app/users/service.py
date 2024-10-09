from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import Session
from app.service.base import BaseService
from app.users.models import User


class UserService(BaseService):
    model = User

    @classmethod
    async def find_full_user_data_or_none(cls, username: str) -> dict | None:
        async with Session() as session:
            query = select(cls.model).options(joinedload(cls.model.role)).where(cls.model.username == username)
            result = await session.execute(query)
            user_info = result.scalar_one_or_none()

            if not user_info:
                return None

            user_data = user_info.to_dict()
            user_data["role"] = user_info.role.name
            return user_data

    @classmethod
    async def find_all(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).options(joinedload(cls.model.role)).filter_by(**filter_by)
            users = await session.execute(query)
            result = []
            for user in users.scalars().all():
                user_dict = user.to_dict()
                user_dict['role'] = user.role.name
                result.append(user_dict)
            return result
