from pydantic import Field

from pydantic import BaseModel


class SRoleCreate(BaseModel):
    name: str = Field(..., title="Role name", description="Role name", min_length=3, max_length=50)