from aiogram import Router
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from aiogram.filters import Command
from fluentogram import TranslatorRunner

from app.database.models import User

router = Router()


@router.message(Command("admin"))
async def command_start_handler(
    message: Message, user: User, i18n: TranslatorRunner
) -> None:
    kb = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Админ-панель",
                    web_app=WebAppInfo(url=f"https://automaestro.ru/admin/"),
                )
            ]
        ],
    )
    await message.answer(text="Admin Panel", reply_markup=kb)
