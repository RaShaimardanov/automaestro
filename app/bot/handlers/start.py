from __future__ import annotations

from aiogram import Router
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    CallbackQuery,
)
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner


router = Router()


def start_poll_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Запустить опрос", callback_data="run_poll")
    return kb.as_markup()


@router.message(Command("admin"))
async def command_start_handler(message: Message) -> None:
    kb = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Админ-панель",
                    web_app=WebAppInfo(url=f""),
                )
            ]
        ],
    )
    await message.answer(text="Admin Panel", reply_markup=kb)
