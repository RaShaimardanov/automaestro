import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from celery import Celery

from app.bot.bot import bot
from app.core.config import settings
from app.core.logger import logger

celery_app = Celery(
    main=settings.PROJECT_NAME,
    broker=settings.REDIS.REDIS_URL,
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(["app.services.tasks.messages"])


@celery_app.task
def sending_message(text, chat_id, reply_markup_data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_message_with_keyboard(text, chat_id, reply_markup_data)
    )


async def send_message_with_keyboard(
    text: str, chat_id: int, reply_markup_data: dict
):
    """Отправка сообщения пользователю с клавиатурой."""
    try:
        buttons = reply_markup_data.get("inline_keyboard")
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=button["callback_data"],
                    )
                    for button in row
                ]
                for row in buttons
            ]
        )
        await bot.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error when sending a message in telegram: {e}")
