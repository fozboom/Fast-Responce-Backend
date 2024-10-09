from app.roles.models import Role
from app.service.base import BaseService


class RoleService(BaseService):
    model = Role