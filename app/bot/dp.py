from aiogram import Dispatcher
from aiogram.enums import ChatType
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage

from app.bot.handlers.admin import router
from app.bot.scenes import scenes_list, router_list
from app.bot.middlewares.chat_type import ChatTypeMiddleware
from app.bot.middlewares.lang import LangMiddleware
from app.bot.middlewares.database import DatabaseMiddleware
from app.database.setup import async_session_pool


def _set_middlewares(dp: Dispatcher):
    """Подключение миддлвари к апдейтам"""
    dp.message.middleware(
        ChatTypeMiddleware([ChatType.PRIVATE])
    )  # разрешаем только частный чат
    dp.update.outer_middleware(
        DatabaseMiddleware(async_session_pool)
    )  # передаем данные для работы с БД в хендлеры
    dp.update.outer_middleware(
        LangMiddleware()
    )  # подключаем сервис локализации и передаем в хендлер


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())

    _set_middlewares(dp)

    dp.include_routers(*router_list)
    dp.include_router(router)

    registry = SceneRegistry(dp)
    registry.add(*scenes_list)

    return dp


dp: Dispatcher = create_dispatcher()
