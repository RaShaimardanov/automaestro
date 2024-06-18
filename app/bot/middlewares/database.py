from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    """
    Промежуточное ПО передает объекты пользователя и репозитория в обработчик.
    """

    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            event_from_user = data.get("event_from_user")
            if not event_from_user:
                return await handler(event, data)

            user = await repo.users.get_or_create_user(
                telegram_id=event_from_user.id,
                first_name=event_from_user.first_name,
                last_name=event_from_user.last_name,
            )

            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result
