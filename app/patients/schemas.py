from datetime import date, datetime
from pydantic import Field, field_validator, ConfigDict
from pydantic.main import BaseModel

from app.locations.schema import SLocationCreate, SLocation
from app.patients.models import Gender
import re

example = SLocationCreate(city="Minsk", street="Леонида Беды", house_number=4, apartment_number=4)


class SPatientCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field("Ivanov Nikita", min_length=5, max_length=80, description="Patient's name")
    birth_date: date = Field("2004-11-07", description="Patient's birth date", examples=["YYYY-MM-DD"])
    phone: str = Field("+375339955111", description="Phone number")
    gender: Gender = Field("male", description="Patient's gender")

    @field_validator("birth_date", mode='before')
    def check_birth_date(cls, value: date):
        if value and value >= datetime.now().date():
            raise ValueError("Birth date must be in the past")
        return value

    @field_validator("phone", mode='before')
    def check_phone(cls, value: str):
        if re.match(r"^\+375\d{9}$", value) is None:
            raise ValueError("Phone number must be valid and start with +375")
        return value


class SPatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model_config['from_attributes'] = True
    id: int = Field(..., description="Patient's id")
    name: str = Field(..., description="Patient's name")
    birth_date: date = Field(..., description="Patient's birth date", examples=["YYYY-MM-DD"])
    phone: str = Field(..., description="Phone number")
    location: SLocation = Field(..., description="Patient's location")
