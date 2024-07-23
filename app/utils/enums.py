from enum import Enum


class OrderStatus(Enum):
    SERVICE = "В работе"
    READY = "Готов"
    ISSUED = "Выдан"


class OptionsSmileEnum(Enum):
    CONFUSE = "👎"
    NEUTRAL = "😐"
    CONFIRM = "👍"

    def __str__(self):
        return f"Смайлы 👎 😐 👍"


class OptionsScoreEnum(Enum):
    POOR = "1"
    FAIR = "2"
    AVERAGE = "3"
    GOOD = "4"
    EXCELLENT = "5"

    def __str__(self):
        return f"Оценка 1-5"


class OptionsType(Enum):
    SMILE = OptionsSmileEnum
    SCORE = OptionsScoreEnum
    CUSTOM = None


class PollType(Enum):
    CLIENT = "Опрос клиентов"
    EMPLOYEE = "Опрос сотрудников"
