from enum import Enum


class OrderStatus(Enum):
    service = "В работе"
    ready = "Готов"
    issued = "Выдан"
