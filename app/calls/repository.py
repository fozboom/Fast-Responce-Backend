from app.base_repository import BaseRepository
from app.calls.models import Call

class CallRepository(BaseRepository):
    model = Call

