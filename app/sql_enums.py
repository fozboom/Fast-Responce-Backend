from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = 'admin'
    DOCTOR = 'doctor'
    DRIVER = 'driver'
    OPERATOR = 'operator'

class GenderEnum(str, Enum):
    MALE = "мужчина"
    FEMALE = "женщина"

class StatusEnum(str, Enum):
    REQUEST_CREATED = "Заявка только создана"
    EN_ROUTE = "Вызов в пути"
    ARRIVED = "Вызов прибыл на место"
    CALL_COMPLETED = "Вызов завершен"



class PriorityEnum(int, Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    DEFERRED = 5