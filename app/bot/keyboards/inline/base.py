from aiogram.utils.keyboard import InlineKeyboardBuilder


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
