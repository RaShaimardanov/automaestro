from typing import Optional

from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.employee import (
    register_menu_kb,
    main_menu_employee_kb,
)
from app.database.models import Employee
from app.database.repo.requests import RequestsRepo
from app.bot.scenes.mixins import MenuScene


class MainMenuEmployeeScene(MenuScene, state="main_menu_employee"):
    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):

        if not employee:
            await message.answer(
                text=i18n.register.employee(), reply_markup=register_menu_kb()
            )
            return
        await message.answer(
            text="Главное меню", reply_markup=main_menu_employee_kb()
        )

    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
        message: Optional[Message] = None,
    ):
        if message:
            await message.answer(
                text="Главное меню", reply_markup=main_menu_employee_kb()
            )
            return
        await callback_query.message.edit_text(
            text="Главное меню", reply_markup=main_menu_employee_kb()
        )
