from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.models import User
from app.database.repo.requests import RequestsRepo


class EmployeeMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        repo: RequestsRepo = data.get("repo")
        user: User = data.get("user")
        data["employee"] = await repo.employees.get_employee(
            telegram_id=user.telegram_id
        )
        result = await handler(event, data)
        return result
