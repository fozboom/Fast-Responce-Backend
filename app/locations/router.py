from fastapi import APIRouter, Security, status, HTTPException, Depends
from typing import List
from app.locations.models import Location
from app.locations.schema import SLocationCreate, SLocation, SCoordinates
from app.locations.service import LocationService
from app.users.auth import role_required
from app.utils.google_maps import gmaps
from app.locations.schema import SLocationUpdate

router = APIRouter(prefix="/locations", tags=["Work with locations"])


@router.post("/add", description="Create new location")
async def create_location(
    location: SLocationCreate = Depends(),
    security_scopes=Security(role_required, scopes=["admin"]),
) -> SLocation:

    in_database = await LocationService.find_one_or_none(**location.model_dump())
    if in_database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Location already exists."
        )
    new_location = await LocationRepository.get_or_create_location_with_geocode(
        **location.model_dump()
    )

    if new_location.id:
        return SLocation.model_validate(new_location)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location could not be created.",
        )


@router.get("/all", description="Get all locations")
async def get_all_locations(
    security_scopes=Security(role_required, scopes=["admin"])
) -> List[SLocation]:
    result = await LocationRepository.find_all()
    return [SLocation.model_validate(location) for location in result]


@router.put("/update/{location_id}", description="Update location")
async def update_location(
    location_id: int,
    location: SLocationUpdate = Depends(),
    security_scopes=Security(role_required, scopes=["admin", "doctor", "operator"]),
) -> SLocation:
    location = await LocationService.update_location_by_id(
        location_id=location_id, **location.model_dump()
    )
    return SLocation.model_validate(location)


@router.get("/current_coordinates", description="Get current coordinates")
async def get_static_coordinates():
    # Возвращаем захардкоженные координаты центра Минска
    return SCoordinates(latitude=53.9, longitude=27.5667)
