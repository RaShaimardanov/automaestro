import json
from typing import Dict

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.utils.enums import MenuOptions, EstimationsEnum
from app.bot.utils.callback_data import (
    MenuActionCallback,
    NotificationsCallback,
    EstimationsCallback,
)


def back_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="« Назад",
        callback_data="back",
    )
    builder.adjust(1)
    return builder


def main_menu_user_kb(context: Dict[str, str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for scene, data in context.items():
        if data:
            builder.button(
                text=MenuOptions[scene].text,
                callback_data=MenuActionCallback(
                    action=MenuOptions[scene].name,
                    context=data,
                ),
            )
    builder.adjust(1)
    return builder.as_markup()


def profile_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=MenuOptions.REGISTER.text,
        callback_data=MenuActionCallback(action=MenuOptions.REGISTER.name),
    )
    builder.button(
        text=MenuOptions.NOTIFICATIONS.text,
        callback_data=MenuActionCallback(
            action=MenuOptions.NOTIFICATIONS.name
        ),
    )
    builder.attach(back_kb())
    builder.adjust(1)
    return builder.as_markup()


def configuration_notifications(
    position: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not position:
        builder.button(
            text="Уведомить о готовности",
            callback_data=NotificationsCallback(position=True),
        )
    else:
        builder.button(
            text="Не уведомлять",
            callback_data=NotificationsCallback(position=False),
        )
    builder.attach(back_kb())
    builder.adjust(1)
    return builder.as_markup()


def offer_receive_notifications() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Уведомить о готовности",
        callback_data=NotificationsCallback(position=True),
    )
    builder.button(
        text="Не уведомлять",
        callback_data=NotificationsCallback(position=False),
    )
    builder.adjust(1)
    return builder.as_markup()


def notifications_settings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Уведомить о готовности",
        callback_data=NotificationsCallback(position=True),
    )
    builder.button(
        text="Не уведомлять",
        callback_data=NotificationsCallback(position=False),
    )
    builder.adjust(1)
    return builder.as_markup()


def csat_kb(visit_id: int):
    builder = InlineKeyboardBuilder()
    for estimation in EstimationsEnum:
        builder.button(
            text=estimation.smile,
            callback_data=EstimationsCallback(
                score=estimation.score, visit_id=visit_id
            ),
        )
    return builder.as_markup()


def accept_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Принято!",
        callback_data=MenuActionCallback(action=MenuOptions.MAIN_MENU.name),
    )
    return builder.as_markup()
