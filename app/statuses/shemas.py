from pydantic import Field, BaseModel


class SStatus(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=100)

