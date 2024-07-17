from aiogram import Dispatcher
from aiogram.enums import ChatType
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage

from app.bot.handlers.admin import router
from app.bot.middlewares.chat_type import ChatTypeMiddleware
from app.database.setup import async_session_pool
from app.bot.scenes import scenes_list, router_list
from app.bot.middlewares.lang import LangMiddleware
from app.bot.middlewares.database import DatabaseMiddleware


def _set_middlewares(dp: Dispatcher):
    dp.message.middleware(ChatTypeMiddleware([ChatType.PRIVATE]))
    dp.update.outer_middleware(DatabaseMiddleware(async_session_pool))
    dp.update.outer_middleware(LangMiddleware())


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())

    _set_middlewares(dp)

    dp.include_router(*router_list)
    dp.include_router(router)

    registry = SceneRegistry(dp)
    registry.add(*scenes_list)

    return dp


dp: Dispatcher = create_dispatcher()
