

from pydantic import BaseModel, Field


class SLocationCreate(BaseModel):
    city: str = Field('Minsk', min_length=1, max_length=50, description='City name')
    street: str = Field('Леонида Беды', min_length=1, max_length=50, description='Street name')
    house_number: int = Field(4, ge=1, le=1000, description='House number')
    apartment_number: int | None = Field(None, ge=1, le=1000, description='Apartment number')


