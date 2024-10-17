from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Session
from app.locations.schema import SLocationCreate
from app.patients.models import Patient
from app.service.base import BaseService
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.locations.models import Location


class PatientService(BaseService):
    model = Patient

    @classmethod
    async def get_or_create_location(cls, **location_data):
        async with Session() as session:
            query = select(Location).filter_by(**location_data)
            result = await session.execute(query)
            location = result.scalar_one_or_none()

            if not location:
                location = Location(**location_data)
                session.add(location)
                await session.flush()


            return location

    @classmethod
    async def add_patient(cls, patient_data, location_data):
        async with Session() as session:
            location = await cls.get_or_create_location(**location_data)

            new_patient_data = patient_data
            new_patient_data["location_id"] = location.id

            new_patient = cls.model(**new_patient_data)
            session.add(new_patient)
            await session.flush()

            query = select(Patient).options(joinedload(Patient.location)).filter_by(id=new_patient.id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with Session() as session:
            query = select(cls.model).options(joinedload(cls.model.location)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
