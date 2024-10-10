from fastapi import APIRouter, Security, status, HTTPException, Depends

from app.locations.models import Location
from app.locations.schema import SLocationCreate
from app.locations.service import LocationService
from app.users.auth import role_required
from app.calls.router import gmaps
router = APIRouter(prefix="/locations", tags=["Work with locations"])


@router.post("/add", description="Create new location")
async def create_location(
        location: SLocationCreate = Depends(),
        security_scopes=Security(role_required, scopes=['admin'])
):
    in_database = await LocationService.find_one_or_none(city=location.city, street=location.street,
                                                   house_number=location.house_number)
    if in_database:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location already exists")
    to_create = location.model_dump()
    address = f"{location.street}, {location.house_number}, {location.city}, Belarus"
    geocode_result = gmaps.geocode(address,
                                   components={"country": "BY"},
                                   region="by",
                                   language="ru")
    to_create['longitude'] = geocode_result[0]["geometry"]["location"]["lng"]
    to_create['latitude'] = geocode_result[0]["geometry"]["location"]["lat"]

    result  = await LocationService.add(**to_create)
    return result

@router.get("/all", description="Get all locations")
async def get_all_locations(security_scopes=Security(role_required, scopes=['admin'])):
    return await LocationService.find_all()