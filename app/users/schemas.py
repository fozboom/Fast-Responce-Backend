from pydantic import BaseModel, ConfigDict
from pydantic import Field


class SUserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Login must be between 4 and 20 characters")
    password: str = Field(..., min_length=4, max_length=20, description="Password must be between 4 and 20 characters")

class SUserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Login must be between 4 and 20 characters")
    password: str = Field(..., min_length=4, max_length=20, description="Password must be between 4 and 20 characters")

class SToken(BaseModel):
    access_token: str
    token_type: str


class STokenData(BaseModel):
    username: str | None = None