from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.bot.handlers.start import router


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher


def init_bot() -> Bot:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=settings.BOT_PARSE_MODE,
            protect_content=settings.BOT_PROTECT_CONTENT,
        ),
    )
    return bot


dispatcher: Dispatcher = create_dispatcher()
bot: Bot = init_bot()
