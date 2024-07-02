from typing import Optional, Any

from aiogram.filters.callback_data import CallbackData


class MenuActionCallback(CallbackData, prefix="action"):
    action: str
    context: Optional[Any] = None


class NotificationsCallback(CallbackData, prefix="position"):
    position: bool


class PollCallback(CallbackData, prefix="poll"):
    poll_id: int


class AnswerCallback(CallbackData, prefix="answer"):
    option: str
    poll_id: int
    question_id: int
