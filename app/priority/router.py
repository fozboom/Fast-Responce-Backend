from fastapi import APIRouter, Security, HTTPException, status, Depends

from app.priority.schemas import SPriorityCreate
from app.priority.service import PriorityService
from app.users.auth import role_required

router = APIRouter(prefix="/priorities", tags=["Work with priorities"])

@router.post("/add", description="Add a new priority")
async def add_priority(
        new_priority: SPriorityCreate = Depends(),
        security_scopes=Security(role_required, scopes=['admin'])
):
    existing_name = await PriorityService.find_one_or_none(name=new_priority.name)

    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Priority with this name already exists",
        )

    existing_level = await PriorityService.find_one_or_none(level=new_priority.level)

    if existing_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Priority with this level already exists",
        )

    return await PriorityService.add(**new_priority.model_dump())

@router.get("/get", description="Get all priorities")
async def get_priorities():
    return await PriorityService.find_all()