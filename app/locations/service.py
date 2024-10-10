from app.locations.models import Location
from app.service.base import BaseService


class LocationService(BaseService):
    model = Location

