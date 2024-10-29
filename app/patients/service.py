from sqlalchemy.ext.asyncio import AsyncSession

from app.database import connection
from app.locations.repository import LocationRepository
from app.locations.service import LocationService
from app.patients.repository import PatientRepository
from app.patients.schemas import SPatientResponse


class PatientService:

    @staticmethod
    async def add_patient(session: AsyncSession, patient_data: dict, location_data: dict):
        location_data.pop('id', None)
        location = await LocationRepository.get_or_create_location_with_geocode(session, location_data)

        new_patient_data = patient_data
        new_patient_data["location_id"] = location.id

        new_patient = await PatientRepository.add_one(session, new_patient_data)

        return SPatientResponse.model_validate(new_patient)
