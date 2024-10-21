from fastapi import APIRouter, Depends, status, HTTPException, Security

from app.locations.service import LocationService
from app.users.auth import role_required
from app.patients.models import Patient
from app.patients.schemas import SPatientResponse
from app.patients.schemas import SPatientCreate
from app.patients.repository import PatientRepository
from app.locations.schema import SLocationCreate
from app.patients.service import PatientService

router = APIRouter(prefix="/patients", tags=["Work with patients"])


@router.post("/add", description="Add new patient")
async def add_patient(
        patient_data: SPatientCreate = Depends(),
        patient_location: SLocationCreate = Depends(),
        security_scopes=Security(role_required, scopes=["admin", "doctor"]),
) -> SPatientResponse:
    new_patient = await PatientService.add_patient(patient_data=patient_data.model_dump(),
                                                   location_data=patient_location.model_dump())
    return new_patient


@router.get("/get", description="Get all patients")
async def get_patients(
        security_scopes=Security(role_required, scopes=["admin", "doctor"]),
) -> list[SPatientResponse]:
    patients = await PatientRepository.find_all()
    return [SPatientResponse.model_validate(patient) for patient in patients]
