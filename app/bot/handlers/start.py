from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from fluentogram import TranslatorRunner

from app.database.models import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(
    message: Message, user: User, i18n: TranslatorRunner
) -> None:
    await message.answer(text=i18n.cmd.start(user=user.first_name))
