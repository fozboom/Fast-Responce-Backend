from sqlalchemy.ext.asyncio import AsyncSession
from app.database import connection


class LocationService:
    @staticmethod
    @connection
    async def get_or_create_location_with_geocode(
        session: AsyncSession, location_data: dict
    ):
        return await LocationRepository.get_or_create_location_with_geocode(
            session, **location_data
        )


