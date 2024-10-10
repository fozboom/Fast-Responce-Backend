from fastapi import APIRouter, Security, Depends

from app.calls.schemas import SCallCreate, SCallForNotify
from app.config import settings
from app.users.auth import role_required

import googlemaps

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

router = APIRouter(prefix="/calls", tags=["Operator actions"])


@router.post("/add", description="Create new call")
async def create_call(
        information: SCallCreate = Depends(),
        security_scopes=Security(role_required, scopes=["operator", "admin"])
):
    informationToNotify = information.model_dump()
    address = f"{information.street}, {information.house_number}, {information.city}, Belarus"

    geocode_result = gmaps.geocode(address,
                                   components={"country": "BY"},
                                   region="by",
                                   language="ru")

    informationToNotify["longitude"] = geocode_result[0]["geometry"]["location"]["lng"]
    informationToNotify["latitude"] = geocode_result[0]["geometry"]["location"]["lat"]

    return SCallForNotify(**informationToNotify)
