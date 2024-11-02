from sqlalchemy.ext.asyncio import AsyncSession

from app.calls.repository import CallRepository
from app.calls.schemas import SCallCreate, SCallData, SDetailedCallInfo, SSimpleCallInfo
from app.database import connection
from app.locations.repository import LocationRepository

from app.locations.service import LocationService
from app.calls.models import Call
from app.patients.repository import PatientRepository
from app.patients.schemas import SPatientCreate
from app.patients.service import PatientService


class CallService:

    @staticmethod
    @connection
    async def create_call(session: AsyncSession, patient_data: SCallCreate):
        location_data = {
            "street": patient_data.street,
            "house_number": patient_data.house_number,
            "city": patient_data.city,
        }
        location = await LocationRepository.get_or_create_location_with_geocode(
            session=session, location_data=location_data
        )
        patient = await PatientRepository.find_one_or_none(
            session, name=patient_data.name
        )
        print(f"Patient: {patient}")
        if not patient:
            patient_create_data = SPatientCreate(
                name=patient_data.name,
                birth_date=patient_data.birth_date,
                gender=patient_data.gender,
                phone=patient_data.phone,
            )
            patient = await PatientService.add_patient(
                session,
                patient_data=patient_create_data.model_dump(),
                location_data=location.to_dict(),
            )

        print(f"Patient: {patient}")

        new_call = SCallData(
            **patient_data.model_dump(), location_id=location.id, patient_id=patient.id
        )

        await CallRepository.add_one(session, new_call.model_dump())

        return new_call

    @staticmethod
    @connection
    async def find_patient_by_name(session: AsyncSession, name: str):
        return await CallRepository.find_all(session, name=name)

    @staticmethod
    @connection
    async def get_all_calls(session: AsyncSession):
        return await CallRepository.find_all(session)

    @staticmethod
    @connection
    async def get_call_details(
        session: AsyncSession,
        call_id: int,
    ) -> SDetailedCallInfo | None:
        call = await CallRepository.find_one_or_none(session=session, id=call_id)
        if not call:
            return None

        patient = await PatientRepository.find_one_or_none(session, id=call.patient_id)
        detailed_call = SDetailedCallInfo.model_validate(patient).model_dump()
        detailed_call["diagnosis"] = call.diagnosis
        detailed_call["description"] = call.description

        old_calls = await CallRepository.find_all(
            session=session, patient_id=call.patient_id
        )
        detailed_call["old_calls"] = [
            SSimpleCallInfo.model_validate(call).model_dump() for call in old_calls
        ]

        return SDetailedCallInfo(**detailed_call)
