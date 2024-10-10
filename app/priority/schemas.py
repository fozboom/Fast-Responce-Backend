from pydantic import BaseModel, Field


class SPriorityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    description: str = Field(..., min_length=1, max_length=120)
    level: int = Field(..., ge=1, le=10)