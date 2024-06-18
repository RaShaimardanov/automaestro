from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluentogram import TranslatorRunner

from app.services.fluent import FluentService, configure_fluent


class LangMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_from_user = data.get("event_from_user")
        fluent: FluentService = configure_fluent()
        translator_runner: TranslatorRunner = fluent.get_translator_by_locale(
            event_from_user.language_code
        )
        data["i18n"] = translator_runner
        return await handler(event, data)