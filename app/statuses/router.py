from fastapi import APIRouter, Depends, Security, HTTPException, status as http_status

from app.logger import logger
from app.statuses.models import Status
from app.statuses.service import StatusService
from app.statuses.shemas import SStatus
from app.users.auth import role_required

router = APIRouter(prefix="/statuses", tags=["Work with statuses"])


@router.post("/add", response_model=SStatus, description="Create new status")
async def create_status(
        status: SStatus = Depends(),
        security_scopes=Security(role_required, scopes=['admin'])
) -> Status:
    existing_status = await StatusService.find_one_or_none(name=status.name)
    logger.debug(f"Existing status: {existing_status}")
    if existing_status:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Status already exists"
        )
    new_status = await StatusService.add(name=status.name, description=status.description)
    return new_status


@router.get("/get", response_model=list[SStatus], description="Get all statuses")
async def get_statuses(security_scopes=Security(role_required, scopes=['admin'])) -> list[Status]:
    statuses = await StatusService.find_all()
    return statuses
