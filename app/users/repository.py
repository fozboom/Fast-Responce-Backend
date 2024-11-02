from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.base_repository import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository):
    model = User



