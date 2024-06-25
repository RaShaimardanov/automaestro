from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_profile(slug_poll: str = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if slug_poll:
        kb.button(text="Запустить опрос", callback_data=slug_poll)
    kb.button(text="Профиль", callback_data="profile")
    kb.adjust(1)
    return kb.as_markup()
