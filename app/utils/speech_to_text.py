import io

from aiogram import Bot
from aiogram.types import Voice
from pydub import AudioSegment
import whisper

from app.core.paths import VOICES_DIR


async def transcribe_voice(bot: Bot, voice: Voice, user_id: int):
    file_path = await save_voice_as_mp3(bot=bot, voice=voice, user_id=user_id)
    text = await audio_to_text(file_path=file_path)
    return text


async def save_voice_as_mp3(bot: Bot, voice: Voice, user_id: int) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)

    voice_path = f"{VOICES_DIR}/voice-{user_id}-{voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        voice_path, format="mp3"
    )
    return voice_path


async def audio_to_text(file_path: str) -> str:
    """Принимает путь к аудио файлу, возвращает текст файла."""
    model = whisper.load_model("small")
    result = model.transcribe(file_path, fp16=False)
    return result["text"]
