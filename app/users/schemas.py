from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from pydantic import Field

from app.sql_enums import RoleEnum, GenderEnum
import re


class SUserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Username for new user")
    full_name: str = Field("Гнетецкий Даниель Геннадьевич", min_length=10, max_length=120,
                           description="Full name of new user")
    password: str = Field(..., min_length=4, max_length=20, description="Password for new user")
    role: RoleEnum = Field(..., description="Role for new user (admin, doctor, etc.)")
    gender: GenderEnum = Field(..., description="Gender of user")
    birth_date: date = Field("2004-11-07", description="User's birth date", examples=["YYYY-MM-DD"])
    address: str = Field("ул. Леонида Беды, д. 4", description="User's address")
    phone: str = Field("+375339955111", description="User's phone number")
    email: EmailStr = Field("email@example.com", description="User's email")

    @classmethod
    @field_validator("birth_date", mode='before')
    def check_birth_date(cls, value: date):
        if value and value >= datetime.now().date():
            raise ValueError("Birth date must be in the past")
        return value

    @classmethod
    @field_validator("phone", mode='before')
    def check_phone(cls, value: str):
        if re.match(r"^\+375\d{9}$", value) is None:
            raise ValueError("Phone number must be valid and start with +375")
        return value


class SUserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Username of authenticated user")
    full_name: str = Field("Гнетецкий Даниель Геннадьевич", min_length=10, max_length=120,
                           description="Full name of new user")
    role: RoleEnum = Field(..., description="Role for new user (admin, doctor, etc.)")
    gender: GenderEnum = Field(..., description="Gender of user")
    birth_date: date = Field("2004-11-07", description="User's birth date", examples=["YYYY-MM-DD"])
    address: str = Field("ул. Леонида Беды, д. 4", description="User's address")
    phone: str = Field("+375339955111", description="User's phone number")
    email: EmailStr = Field("email@example.com", description="User's email")


class SToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str



class STokenData(BaseModel):
    username: str | None = None
