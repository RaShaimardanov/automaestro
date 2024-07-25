from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.keyboards.inline.base import build_keyboard
from app.bot.utils.callback_data import (
    ChangeStatusCallback,
    MenuActionCallback,
)
from app.bot.utils.enums import MenuOptions
from app.utils.enums import OrderStatus


def main_menu_employee_kb(visits) -> InlineKeyboardMarkup:
    """Клавиатура главного меню сотрудника"""
    buttons = []
    if visits:
        buttons.append(
            InlineKeyboardButton(
                text=MenuOptions.WORK_SCENE.text,
                callback_data=MenuActionCallback(
                    action=MenuOptions.WORK_SCENE.name
                ).pack(),
            )
        )
    buttons.append(
        InlineKeyboardButton(
            text=MenuOptions.PROFILE_EMPLOYEE.text,
            callback_data=MenuActionCallback(
                action=MenuOptions.PROFILE_EMPLOYEE.name
            ).pack(),
        ),
    )
    return build_keyboard(buttons)


def register_menu_kb() -> InlineKeyboardMarkup:
    """Кнопка запуска сцены регистрации сотрудника"""
    buttons = [
        InlineKeyboardButton(
            text=MenuOptions.REGISTER_EMPLOYEE.text,
            callback_data=MenuActionCallback(
                action=MenuOptions.REGISTER_EMPLOYEE.name
            ).pack(),
        )
    ]
    return build_keyboard(buttons)


def profile_menu_kb() -> InlineKeyboardMarkup:
    """Клавиатура меню профиля сотрудника"""
    buttons = [
        InlineKeyboardButton(
            text="Обновить контактные данные",
            callback_data=MenuActionCallback(
                action=MenuOptions.REGISTER_EMPLOYEE.name
            ).pack(),
        ),
        InlineKeyboardButton(
            text="Получить QR-code",
            callback_data="qrcode",
        ),
    ]
    return build_keyboard(buttons, include_back=True)


def work_menu_kb(visits) -> InlineKeyboardMarkup:
    """Клавиатура с автомобилями которые находятся в работе у сотрудика"""
    buttons = [
        InlineKeyboardButton(
            text=f"{visit.user.car.license_plate_number} • {visit.status.value}",
            callback_data=MenuActionCallback(
                action=MenuOptions.WORK_DETAIL.name, context=visit.id
            ).pack(),
        )
        for visit in visits
    ]
    return build_keyboard(buttons, include_back=True)


def work_detail_menu_kb(visit) -> InlineKeyboardMarkup:
    """Клавиатура с функциями изменения статуса автомобиля"""
    buttons = []
    if visit.status == OrderStatus.SERVICE:
        smile = "🔔" if visit.notify_ready else "🔕"
        buttons.append(
            InlineKeyboardButton(
                text=f"{smile} Автомобиль готов",
                callback_data=ChangeStatusCallback(
                    visit_id=visit.id, status=OrderStatus.READY.name
                ).pack(),
            )
        )
    buttons.append(
        InlineKeyboardButton(
            text="✅ Автомобиль выдан",
            callback_data=ChangeStatusCallback(
                visit_id=visit.id, status=OrderStatus.ISSUED.name
            ).pack(),
        )
    )
    return build_keyboard(buttons, include_back=True)
