import json

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.utils.enums import MenuOptions
from app.bot.utils.callback_data import (
    MenuActionCallback,
    NotificationsCallback,
)


def back_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="« Назад",
        callback_data="back",
    )
    builder.adjust(1)
    return builder


def main_menu_user_kb(context) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if context:
        builder.button(
            text=MenuOptions.POLL.text,
            callback_data=MenuActionCallback(
                action=MenuOptions.POLL.name, context=context
            ),
        )
    builder.button(
        text=MenuOptions.PROFILE.text,
        callback_data=MenuActionCallback(action=MenuOptions.PROFILE.name),
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
