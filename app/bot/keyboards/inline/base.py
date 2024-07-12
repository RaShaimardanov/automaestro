from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def update_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Обновить",
        callback_data="update",
    )
    builder.adjust(1)
    return builder


def back_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="« Назад",
        callback_data="back",
    )
    builder.adjust(1)
    return builder


def build_keyboard(
    buttons: List[InlineKeyboardButton],
    width: int = 1,
    include_back: bool = False,
) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    for button in buttons:
        builder.button(text=button.text, callback_data=button.callback_data)

    if include_back:
        builder.attach(back_kb())

    builder.adjust(width)
    return builder.as_markup()
