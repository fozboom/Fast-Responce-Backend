from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Session
from app.locations.models import Location
from app.service.base import BaseService
from app.calls.router import gmaps
from sqlalchemy import select

class LocationService(BaseService):
    model = Location

    @classmethod
    async def get_or_create_location_with_geocode(cls, **location_data):
        async with Session() as session:
            query = select(Location).filter_by(**location_data)
            result = await session.execute(query)
            location = result.scalar_one_or_none()

            if location:
                return location

            address = f"{location_data['street']}, {location_data['house_number']}, {location_data['city']}, Belarus"

            try:
                geocode_result = gmaps.geocode(
                    address,
                    components={"country": "BY"},
                    region="by",
                    language="ru"
                )

                if not geocode_result:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not find coordinates for the given address.")

                location_data['longitude'] = geocode_result[0]["geometry"]["location"]["lng"]
                location_data['latitude'] = geocode_result[0]["geometry"]["location"]["lat"]

                new_location = Location(**location_data)
                session.add(new_location)
                await session.flush()

                await session.commit()

                return new_location

            except googlemaps.exceptions.ApiError as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Geocoding API error: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

