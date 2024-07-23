import asyncio

from app.services.tasks.apps import celery_app
from app.utils.send_message import send_message_with_keyboard
from app.utils.speech_to_text import audio_to_text

celery = celery_app


@celery.task
def send_message_task(text, chat_id, reply_markup_data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        send_message_with_keyboard(text, chat_id, reply_markup_data)
    )


@celery.task
def transcribe_voice_task(voice_path):
    text = audio_to_text(voice_path)
    return text
