from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry

from app.bot.handlers.start import router as admin_router
from app.core.config import settings
from app.bot.scenes import scenes_list
from app.database.setup import async_session_pool
from app.bot.middlewares.lang import LangMiddleware
from app.bot.middlewares.database import DatabaseMiddleware


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    dp = Dispatcher()
    dp.update.outer_middleware(DatabaseMiddleware(async_session_pool))
    dp.update.outer_middleware(LangMiddleware())
    dp.include_router(admin_router)

    registry = SceneRegistry(dp)
    registry.add(*scenes_list)

    return dp


def init_bot() -> Bot:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=settings.BOT_PARSE_MODE,
            protect_content=settings.BOT_PROTECT_CONTENT,
        ),
    )

    return bot


dp: Dispatcher = create_dispatcher()
bot: Bot = init_bot()
