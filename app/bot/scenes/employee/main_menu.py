from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline import employee as kb
from app.bot.scenes.mixins import MenuScene
from app.core.logger import logger
from app.database.models import Employee
from app.database.repo.requests import RequestsRepo


class MainMenuEmployeeScene(MenuScene, state="main_menu_employee"):
    """Сцена отправки главного меню сотрудника"""

    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """Вход в сцену через сообщение/команду"""
        try:
            if not employee:
                # если пользователь не зарегестрирован в качетсве сотрудника
                # отправляем предложение зарегестрироваться
                await message.answer(
                    text=i18n.register.employee(),
                    reply_markup=kb.register_menu_kb(),
                )
                return
            visits = await repo.visits.get_current_visits_by_employee_id(
                employee_id=employee.id
            )
            message = await message.answer(
                text=i18n.employee.main.menu(total=len(visits)),
                reply_markup=kb.main_menu_employee_kb(visits),
            )
            await self.wizard.update_data(message=message)
        except Exception as e:
            logger.error(f"Error menu message {employee.telegram_id}: {e}")

    @on.callback_query.enter()
    async def on_callback_enter(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """Вход в сцену через коллбэк"""
        visits = await repo.visits.get_current_visits_by_employee_id(
            employee_id=employee.id
        )
        try:
            message = await callback_query.message.edit_text(
                text=i18n.employee.main.menu(total=len(visits)),
                reply_markup=kb.main_menu_employee_kb(visits),
            )
            await self.wizard.update_data(message=message)

        except TelegramBadRequest as e:
            # если предыдущее сообщение было удалено
            if "message to edit not found" in str(e):
                message = await callback_query.bot.send_message(
                    chat_id=employee.telegram_id,
                    text=i18n.employee.main.menu(total=len(visits)),
                    reply_markup=kb.main_menu_employee_kb(visits),
                )
                await self.wizard.update_data(message=message)
            else:
                logger.error(f"Error menu message {employee.telegram_id}: {e}")

        except Exception as e:
            logger.error(f"Error menu message {employee.telegram_id}: {e}")
