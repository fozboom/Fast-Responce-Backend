from pydantic import BaseModel, ConfigDict, Field


class SCallCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., min_length=3, max_length=80, description="Full name of patient, which need help")
    city: str = Field(..., min_length=3, max_length=80, description="City of patient")
    street: str = Field(..., min_length=3, max_length=80, description="Street address of patient")
    house_number: int = Field(..., description="House number of patient")
    apartment_number: int | None = Field(None, description="Apartment number of patient")
    diagnosis: str | None = Field(None, min_length=0, max_length=80, description="Diagnosis of patient")
    description: str | None = Field(None, min_length=0, max_length=80, description="Description of patient's condition")


class SCallForNotify(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., min_length=3, max_length=80, description="Full name of patient, which need help")
    city: str = Field(..., min_length=3, max_length=80, description="City of patient")
    street: str = Field(..., min_length=3, max_length=80, description="Street address of patient")
    house_number: int = Field(..., description="House number of patient")
    apartment_number: int | None = Field(None, description="Apartment number of patient")
    diagnosis: str | None = Field(None, min_length=0, max_length=80, description="Diagnosis of patient")
    description: str | None = Field(None, min_length=0, max_length=80, description="Description of patient's condition")
    longitude: float = Field(..., description="Longitude of patient's location")
    latitude: float = Field(..., description="Latitude of patient's location")