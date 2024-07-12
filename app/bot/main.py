from aiogram import Dispatcher
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage

from app.database.setup import async_session_pool
from app.bot.scenes import scenes_list, router_list
from app.bot.middlewares.lang import LangMiddleware
from app.bot.middlewares.database import DatabaseMiddleware


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    # redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    # storage = RedisStorage(
    #     redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    # )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    dp.update.outer_middleware(DatabaseMiddleware(async_session_pool))
    dp.update.outer_middleware(LangMiddleware())
    dp.include_router(*router_list)

    registry = SceneRegistry(dp)
    registry.add(*scenes_list)

    return dp


dp: Dispatcher = create_dispatcher()
