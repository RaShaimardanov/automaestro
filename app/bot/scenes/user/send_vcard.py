from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from app.bot.scenes.mixins import MenuScene
from app.core.logger import logger
from app.database.models import Employee
from app.database.repo.requests import RequestsRepo


class SendVCardScene(MenuScene, state="visit_card"):
    """Сцена отправки контакта сотрудника"""

    @on.callback_query.enter()
    async def send_vcard(
        self,
        callback_query: CallbackQuery,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
        context: str,
    ):
        """Функция отправки контакта сотрудника"""
        try:
            employee: Employee = await repo.employees.get(int(context))

            vcard = i18n.vcard(
                last_name=employee.last_name,
                first_name=employee.first_name,
                phone_number=employee.phone_number,
                email=employee.email,
            )
            await callback_query.message.answer_contact(
                phone_number=f"{employee.phone_number}",
                first_name=f"{employee.first_name}",
                last_name=f"{employee.last_name}",
                vcard=vcard,
            )

            await self.wizard.back()

        except Exception as e:
            logger.error(f"Error send vcard: {e}")
