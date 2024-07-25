from typing import Any, Optional

from aiogram.filters.callback_data import CallbackData


class MenuActionCallback(CallbackData, prefix="action"):
    action: str
    context: Optional[Any] = None


class ChangeStatusCallback(CallbackData, prefix="status"):
    visit_id: int
    status: str


class NotificationsCallback(CallbackData, prefix="position"):
    position: bool
    visit_id: int


class PollCallback(CallbackData, prefix="poll"):
    poll_id: int
    questions_quantity: int


class EstimationsCallback(CallbackData, prefix="estimation"):
    visit_id: int
    score: int


class AnswerCallback(CallbackData, prefix="answer"):
    option: str
    poll_id: int
    question_id: int
    questions_quantity: int
    question_number: int
