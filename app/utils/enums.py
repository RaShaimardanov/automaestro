from enum import Enum


class OrderStatus(Enum):
    SERVICE = "В работе"
    READY = "Готов"
    ISSUED = "Выдан"


class OptionsSmileEnum(Enum):
    CONFUSE = "👎"
    NEUTRAL = "😐"
    CONFIRM = "👍"


class OptionsScoreEnum(Enum):
    POOR = "1"
    FAIR = "2"
    AVERAGE = "3"
    GOOD = "4"
    EXCELLENT = "5"


class OptionsType(Enum):
    SMILE = OptionsSmileEnum
    SCORE = OptionsScoreEnum
    CUSTOM = None


class PollType(Enum):
    CLIENT = "Опрос клиентов"
    EMPLOYEE = "Опрос сотрудников"
