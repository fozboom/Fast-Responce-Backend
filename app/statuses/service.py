from app.service.base import BaseService
from app.statuses.models import Status


class StatusService(BaseService):
    model = Status
    @classmethod
    def to_dict(cls, status: Status) -> dict:
        return {
            "id": status.id,
            "name": status.name,
            "description": status.description
        }