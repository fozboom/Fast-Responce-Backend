

from pydantic import BaseModel, Field, ConfigDict


class SLocationCreate(BaseModel):
    city: str = Field('Минск', min_length=1, max_length=50, description='City name')
    street: str = Field('Леонида Беды', min_length=1, max_length=50, description='Street name')
    house_number: int = Field(4, ge=1, le=1000, description='House number')
    apartment_number: int | None = Field(None, ge=1, le=1000, description='Apartment number')



class SLocation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description='Location ID')
    city: str = Field(..., description='City name')
    street: str = Field(..., description='Street name')
    house_number: int | None = Field(None, description='House number')
    apartment_number: int | None = Field(None, description='Apartment number')
    latitude: float = Field(..., description='Latitude')
    longitude: float = Field(..., description='Longitude')
