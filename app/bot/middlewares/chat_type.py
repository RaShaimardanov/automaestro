from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ChatTypeMiddleware(BaseMiddleware):
    def __init__(self, chat_types: list) -> None:
        self.chat_types = chat_types

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type in self.chat_types:
            return await handler(event, data)
