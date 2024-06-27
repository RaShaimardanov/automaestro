from enum import Enum


class BaseOptionsEnum(Enum):

    @classmethod
    def get_all_values(cls):
        return " ".join([member.value.get("represent") for member in cls])


class OrderStatus(Enum):
    service = "В работе"
    ready = "Готов"
    issued = "Выдан"


class OptionsSmileEnum(BaseOptionsEnum):
    confuse = {"score": 0, "represent": "👎"}
    pristine = {"score": 1, "represent": "😐"}
    confirm = {"score": 2, "represent": "👍"}


class OptionsScoreEnum(BaseOptionsEnum):
    poor = {"score": 1, "represent": "😞"}
    fair = {"score": 2, "represent": "😕"}
    average = {"score": 3, "represent": "😐"}
    good = {"score": 4, "represent": "🙂"}
    excellent = {"score": 5, "represent": "😊"}


class OptionsType(Enum):
    smile = OptionsSmileEnum
    score = OptionsScoreEnum
    custom = None

    def get_all_values(self):
        if self.value is not None:
            return self.value.get_all_values()
