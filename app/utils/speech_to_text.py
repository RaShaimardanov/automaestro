import io

from pydub import AudioSegment
import whisper

from app.bot.bot import bot
from app.core.paths import VOICES_DIR


async def download_and_convert_voice(voice_file_id: str, user_id: int) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(voice_file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)

    voice_path = f"{VOICES_DIR}/voice-{user_id}-{voice_file_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        voice_path, format="mp3"
    )
    return voice_path


def audio_to_text(file_path: str) -> str:
    """Принимает путь к аудио файлу, возвращает текст файла."""
    model = whisper.load_model("medium")
    result = model.transcribe(file_path, fp16=False)
    return result["text"]
