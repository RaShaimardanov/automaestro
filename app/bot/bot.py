from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings


def init_bot() -> Bot:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=settings.BOT_PARSE_MODE,
            protect_content=settings.BOT_PROTECT_CONTENT,
        ),
    )

    return bot


bot: Bot = init_bot()
