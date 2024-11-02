from pydantic import BaseModel, ConfigDict, Field

from app.sql_enums import PriorityEnum, GenderEnum
from datetime import date


class SCallCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        "Иванов Иван Иванович",
        min_length=3,
        max_length=80,
        description="Full name of patient, which need help",
    )
    birth_date: date = Field(
        "2004-11-07", description="Patient's birth date", examples=["YYYY-MM-DD"]
    )
    gender: GenderEnum = Field("мужчина", description="Patient's gender")
    phone: str | None = Field("+375339955111", description="Phone number")

    city: str = Field(
        "Минск", min_length=3, max_length=80, description="City of patient"
    )
    street: str = Field(
        "Леонида Беды",
        min_length=3,
        max_length=80,
        description="Street address of patient",
    )
    house_number: int = Field(4, description="House number of patient")
    apartment_number: int | None = Field(
        None, description="Apartment number of patient"
    )

    diagnosis: str | None = Field(
        None, min_length=0, max_length=80, description="Diagnosis of patient"
    )
    description: str | None = Field(
        None,
        min_length=0,
        max_length=80,
        description="Description of patient's condition",
    )

    driver_name: str | None = Field(
        "Иванов Никита Сергеевич",
        min_length=3,
        max_length=80,
        description="Full name of driver",
    )
    operator_name: str | None = Field(
        "Коваленко Ольга Михайловна",
        min_length=3,
        max_length=80,
        description="Full name of operator",
    )
    doctor_name: str | None = Field(
        "Степанов Игорь Валерьевич",
        min_length=3,
        max_length=80,
        description="Full name of doctor",
    )

    priority: PriorityEnum = Field(..., title="Приоритет вызова")


class SCallForNotify(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(
        ...,
        min_length=3,
        max_length=80,
        description="Full name of patient, which need help",
    )
    city: str = Field(..., min_length=3, max_length=80, description="City of patient")
    street: str = Field(
        ..., min_length=3, max_length=80, description="Street address of patient"
    )
    house_number: int = Field(..., description="House number of patient")
    apartment_number: int | None = Field(
        None, description="Apartment number of patient"
    )
    diagnosis: str | None = Field(
        None, min_length=0, max_length=80, description="Diagnosis of patient"
    )
    description: str | None = Field(
        None,
        min_length=0,
        max_length=80,
        description="Description of patient's condition",
    )
    longitude: float = Field(..., description="Longitude of patient's location")
    latitude: float = Field(..., description="Latitude of patient's location")


class SCallData(BaseModel):
    patient_id: int
    location_id: int
    driver_name: str | None
    operator_name: str | None
    doctor_name: str | None
    diagnosis: str | None
    description: str | None
    priority: PriorityEnum
    status: str = Field(default="REQUEST_CREATED")


class SSimpleCallInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    diagnosis: str | None = Field(
        None, min_length=0, max_length=120, description="Diagnosis of patient"
    )
    description: str | None = Field(
        None, min_length=0, max_length=120, description="Description of call"
    )


class SDetailedCallInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        min_length=3,
        max_length=80,
        description="Full name of patient, which need help",
    )
    birth_date: date = Field(
        ..., description="Patient's birth date", examples=["YYYY-MM-DD"]
    )
    gender: GenderEnum = Field("мужчина", description="Patient's gender")
    phone: str | None = Field("+375339955111", description="Phone number")

    diagnosis: str | None = Field(
        None, min_length=0, max_length=120, description="Diagnosis of patient"
    )
    description: str | None = Field(
        None, min_length=0, max_length=120, description="Description of call"
    )

    old_calls: list[SSimpleCallInfo] | None = Field(
        None, description="List of previous calls"
    )
