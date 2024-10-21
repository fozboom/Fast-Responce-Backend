from sqlalchemy.ext.asyncio import AsyncSession

from app.database import connection
from app.sql_enums import GenderEnum
from app.users.repository import UserRepository
from datetime import date


@connection
async def find_all_users(session):
    return await UserRepository.find_all(session)


@connection
async def find_user_by_name(username: str, session: AsyncSession):
    return await UserRepository.find_one_or_none(session, username=username)


@connection
async def add_user(session: AsyncSession, **user_data):
    return await UserRepository.add_one(session, **user_data)

# @connection
# async def save_refresh_token(session: AsyncSession, username: str, refresh_token: str):
#     return await UserRepository.update_refresh_token(session, username=username, refresh_token=refresh_token)
