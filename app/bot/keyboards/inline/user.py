from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.keyboards.inline.base import build_keyboard
from app.bot.utils.enums import MenuOptions, EstimationsEnum
from app.bot.utils.callback_data import (
    MenuActionCallback,
    EstimationsCallback,
    NotificationsCallback,
)


def main_menu_user_kb(context: Dict[str, str]) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=MenuOptions[scene].text,
            callback_data=MenuActionCallback(
                action=MenuOptions[scene].name,
                context=data,
            ).pack(),
        )
        for scene, data in context.items()
        if data
    ]
    return build_keyboard(buttons)


def profile_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=MenuOptions.REGISTER.text,
            callback_data=MenuActionCallback(
                action=MenuOptions.REGISTER.name
            ).pack(),
        ),
        InlineKeyboardButton(
            text=MenuOptions.NOTIFICATIONS.text,
            callback_data=MenuActionCallback(
                action=MenuOptions.NOTIFICATIONS.name
            ).pack(),
        ),
    ]
    return build_keyboard(buttons, include_back=True)


def notifications_setting_kb(
    visit_id: int,
    position: bool = False,
) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="Не уведомлять" if position else "Уведомить о готовности",
            callback_data=NotificationsCallback(
                position=not position, visit_id=visit_id
            ).pack(),
        )
    ]
    return build_keyboard(buttons, include_back=True)


def notifications_receive_kb(visit_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="Уведомить о готовности",
            callback_data=NotificationsCallback(
                position=True, visit_id=visit_id
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Не уведомлять",
            callback_data=NotificationsCallback(
                position=False, visit_id=visit_id
            ).pack(),
        ),
    ]
    return build_keyboard(buttons)


def csat_kb(visit_id: int):
    buttons = [
        InlineKeyboardButton(
            text=estimation.smile,
            callback_data=EstimationsCallback(
                score=estimation.score, visit_id=visit_id
            ).pack(),
        )
        for estimation in EstimationsEnum
    ]
    return build_keyboard(buttons, width=len(EstimationsEnum))


def accept_kb() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="Принято!",
            callback_data=MenuActionCallback(
                action=MenuOptions.MAIN_MENU_USER.name
            ).pack(),
        )
    ]
    return build_keyboard(buttons)
