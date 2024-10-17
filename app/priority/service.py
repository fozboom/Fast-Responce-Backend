from app.priority.models import Priority
from app.roles.models import Role
from app.service.base import BaseService


class PriorityService(BaseService):
    model = Priority