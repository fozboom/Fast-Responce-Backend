from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from app.roles.schemas import SRoleCreate
from app.roles.service import RoleService

router = APIRouter(prefix='/roles', tags=['Work with roles'])

@router.post('/add', description="Add new role")
async def add_role(role_data: SRoleCreate = Depends()) -> SRoleCreate:
    role = await RoleService.find_one_or_none(name=role_data.name)
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already registered",
        )

    new_role = role_data.model_dump()
    await RoleService.add(**new_role)

    return role_data