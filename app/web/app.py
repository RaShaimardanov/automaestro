from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.logger import logger
from app.core.config import settings
from app.bot.main import bot, dispatcher
from app.core.paths import STATIC_FOLDER, IMAGES_DIR
from app.web.api.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для обработки запуска и остановки бота."""
    logger.info("Приложение запущено.")
    await bot.set_webhook(
        url=f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET,
        drop_pending_updates=settings.BOT_DROP_PENDING_UPDATES,
    )

    yield
    await bot.delete_webhook(
        drop_pending_updates=settings.BOT_DROP_PENDING_UPDATES,
    )
    await bot.session.close()
    logger.info("Приложение остановлено.")


def init_app() -> FastAPI:
    """Инициализация и возвращение приложения FastAPI."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    # app.add_middleware(HTTPSRedirectMiddleware)
    app.mount(
        path="/static",
        app=StaticFiles(directory=STATIC_FOLDER),
        name="static",
    )
    app.mount(
        path="/images",
        app=StaticFiles(directory=IMAGES_DIR),
        name="images",
    )
    app.include_router(router)

    return app


app = init_app()


@app.post(path=settings.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    """Функция для приёма сообщений из Telegram."""
    telegram_update = Update(**update)
    response = await dispatcher.feed_update(bot=bot, update=telegram_update)
    logger.info(
        "Update id=%s is %s.",
        telegram_update.update_id,
        "handled" if not response else "not handled",
    )
