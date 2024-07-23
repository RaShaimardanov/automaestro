from aiogram import F
from aiogram.fsm.scene import on
from aiogram.enums import MessageEntityType
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.core.logger import logger
from app.bot.utils.enums import MenuOptions
from app.bot.scenes.mixins import MenuScene
from app.utils.gen_qrcode import generate_qrcode
from app.bot.keyboards.inline.base import update_kb
from app.database.models import User, Employee
from app.database.repo.requests import RequestsRepo


class RegisterEmployeeScene(MenuScene, state="employee_register_scene"):
    """Сцена регистрации и редактирования контактных данных сотрудника"""

    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        user: User,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Вход в сцену. Для регистрации необходимо наличие фамилии в профиле.
        Создает/обновляет модель сотрудника и предлагает ввести номер телефона.
        """
        try:
            if not user.last_name:
                text = i18n.register.employee.suspend()
                if callback_query.message.html_text != text:
                    await callback_query.message.edit_text(
                        text=text,
                        reply_markup=update_kb().as_markup(),
                    )
                else:
                    await callback_query.answer(
                        text=i18n.unchanged.data(), show_alert=True
                    )
                return

            employee_data = {
                "telegram_id": user.telegram_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            if not employee:
                await repo.employees.create(data=employee_data)
            else:
                await repo.employees.update(
                    employee,
                    update_data=employee_data,
                )

            await callback_query.message.edit_text(
                text=i18n.register.scene.input.phone()
            )

        except Exception as e:
            logger.error(
                f"An error occurred for user {user.telegram_id}: {str(e)}"
            )

    @on.message(F.entities[:].type == MessageEntityType.PHONE_NUMBER)
    async def input_phone_number(
        self,
        message: Message,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Функция обработки и сохранения номера телефона.
        Предлагает ввести номер email.
        """
        await repo.employees.update(
            employee, update_data=dict(phone_number=message.text)
        )
        await message.answer(text=i18n.register.scene.input.email())

    @on.message(F.entities[:].type == MessageEntityType.EMAIL)
    async def input_email(
        self,
        message: Message,
        employee: Employee,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Функция обработки и сохранения email.
        По завершению отправляет в главное меню и генерирует QR-код.
        """
        try:
            await repo.employees.update(
                employee, update_data=dict(email=message.text)
            )
            await message.answer(
                text=i18n.register.scene.success(
                    first_name=employee.first_name,
                    last_name=employee.last_name,
                    phone_number=employee.phone_number,
                    email=message.text,
                )
            )
            await self.wizard.goto(MenuOptions.MAIN_MENU_EMPLOYEE.scene)

            await generate_qrcode(parameter=employee.telegram_id)

        except Exception as e:
            logger.error(
                f"Error update data {employee.telegram_id} - {str(e)}"
            )

    @on.message()
    async def unknown_message(
        self,
        message: Message,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает любые другие сообщения и перезапускает сцену"""
        await message.answer(text=i18n.input.data.invalid())
        await self.wizard.retake()
