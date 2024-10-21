from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Session
from app.patients.models import Patient
from app.base_repository import BaseRepository
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.locations.models import Location


class PatientRepository(BaseRepository):
    model = Patient


    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).options(joinedload(cls.model.location)).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()
