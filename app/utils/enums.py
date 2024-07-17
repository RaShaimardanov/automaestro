from enum import Enum


class OrderStatus(Enum):
    service = "В работе"
    ready = "Готов"
    issued = "Выдан"


class OptionsSmileEnum(Enum):
    confuse = "👎"
    pristine = "😐"
    confirm = "👍"


class OptionsScoreEnum(Enum):
    poor = "1"
    fair = "2"
    average = "3"
    good = "4"
    excellent = "5"


class OptionsType(Enum):
    smile = OptionsSmileEnum
    score = OptionsScoreEnum
    custom = None


class PollType(Enum):
    client = "Опрос клиентов"
    employee = "Опрос сотрудников"
