from aiogram import Bot, Dispatcher
from aiogram.fsm.scene import SceneRegistry
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.database.setup import async_session_pool
from app.bot.scenes import scenes_list, router_list
from app.bot.middlewares.lang import LangMiddleware
from app.bot.middlewares.database import DatabaseMiddleware


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(DatabaseMiddleware(async_session_pool))
    dp.update.outer_middleware(LangMiddleware())
    dp.include_router(*router_list)

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
