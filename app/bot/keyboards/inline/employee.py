from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.inline.user import back_kb
from app.bot.utils.callback_data import (
    MenuActionCallback,
    ChangeStatusCallback,
)
from app.bot.utils.enums import MenuOptions
from app.utils.enums import OrderStatus


def main_menu_employee_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=MenuOptions.WORK_SCENE.text,
        callback_data=MenuActionCallback(action=MenuOptions.WORK_SCENE.name),
    )
    builder.button(
        text=MenuOptions.PROFILE_EMPLOYEE.text,
        callback_data=MenuActionCallback(
            action=MenuOptions.PROFILE_EMPLOYEE.name
        ),
    )
    builder.adjust(1)
    return builder.as_markup()


def register_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=MenuOptions.REGISTER_EMPLOYEE.text,
        callback_data=MenuActionCallback(
            action=MenuOptions.REGISTER_EMPLOYEE.name
        ),
    )
    return builder.as_markup()


def profile_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Обновить контактные данные",
        callback_data=MenuActionCallback(
            action=MenuOptions.REGISTER_EMPLOYEE.name
        ),
    )
    builder.button(
        text="Получить QR-code",
        callback_data="qrcode",
    )
    builder.attach(back_kb())
    builder.adjust(1)
    return builder.as_markup()


def work_menu_kb(visits) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for visit in visits:
        builder.button(
            text=f"{visit.user.car.license_plate_number} • {visit.status.value}",
            callback_data=MenuActionCallback(
                action=MenuOptions.WORK_DETAIL.name, context=visit.id
            ),
        )
    builder.attach(back_kb())
    builder.adjust(1)
    return builder.as_markup()


def work_detail_menu_kb(visit) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if visit.status == OrderStatus.service:
        smile = "🔔" if visit.notify_ready else "🔕"
        builder.button(
            text=f"{smile} Автомобиль готов",
            callback_data=ChangeStatusCallback(
                visit_id=visit.id, status=OrderStatus.ready.name
            ),
        )
    builder.button(
        text="✅ Автомобиль выдан",
        callback_data=ChangeStatusCallback(
            visit_id=visit.id, status=OrderStatus.issued.name
        ),
    )
    builder.attach(back_kb())
    builder.adjust(1)
    return builder.as_markup()
