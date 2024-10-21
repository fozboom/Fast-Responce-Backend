import googlemaps

from app.config import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
