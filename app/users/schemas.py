from pydantic import BaseModel, ConfigDict
from pydantic import Field


class SUserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Username for new user")
    password: str = Field(..., min_length=4, max_length=20, description="Password for new user")
    role: str = Field(..., min_length=3, max_length=50, description="Role for new user (admin, doctor, etc.)")

class SUserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., min_length=4, max_length=20, description="Username of authenticated user")
    is_active: bool = Field(..., description="User is active or not")
    role: str = Field(..., min_length=3, max_length=50, description="Role for new user (admin, doctor, etc.)")
class SToken(BaseModel):
    access_token: str
    token_type: str


class STokenData(BaseModel):
    username: str | None = None