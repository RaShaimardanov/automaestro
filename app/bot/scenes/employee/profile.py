from typing import Optional

from aiogram import F
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, FSInputFile, Message
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.employee import profile_menu_kb
from app.bot.scenes.mixins import MenuScene
from app.bot.utils.enums import MenuOptions
from app.core.logger import logger
from app.core.paths import QRCODES_DIR
from app.database.models import Employee


class ProfileEmployeeScene(MenuScene, state="profile_employee"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        i18n: TranslatorRunner,
    ):
        await callback_query.message.edit_text(
            text=i18n.employee.profile.scene.enter(
                first_name=employee.first_name,
                last_name=employee.last_name,
                phone_number=employee.phone_number,
                email=employee.email,
            ),
            reply_markup=profile_menu_kb(),
        )

    @on.callback_query(F.data == "qrcode")
    async def send_qrcode(
        self,
        callback_query: CallbackQuery,
        employee: Employee,
        i18n: TranslatorRunner,
    ):
        try:
            message = await callback_query.message.answer_photo(
                photo=FSInputFile(QRCODES_DIR / f"{employee.telegram_id}.jpg"),
                caption=i18n.employee.profile.scene.qrcode(),
                protect_content=False,
            )
            await callback_query.message.delete()
            await self.wizard.goto(
                MenuOptions.MAIN_MENU_EMPLOYEE.scene, message=message
            )
        except Exception as e:
            logger.error(
                f"Error send QR-code: {employee.telegram_id} - {str(e)}"
            )
