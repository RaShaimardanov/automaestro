from typing import Optional

from aiogram import F
from aiogram.fsm.scene import After, on
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.base import back_kb
from app.bot.scenes.mixins import MenuScene
from app.bot.utils.enums import MenuOptions
from app.core.constants import LICENSE_PLATE_REGEX
from app.core.logger import logger
from app.database.models import User
from app.database.repo.requests import RequestsRepo


class RegisterCarScene(MenuScene, state="register_car"):
    """Сцена для регистрации гос. номера автомобиля"""

    @on.message.enter()
    async def on_enter_register_car(
        self,
        message: Message,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает вход в сцену регистрации гос. номера автомобиля."""
        await message.answer(text=i18n.register.car.scene.enter())

    @on.callback_query.enter()
    async def on_enter_callback_query_register_car(
        self,
        callback_query: CallbackQuery,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает вход в сцену для редактирования гос. номера автомобиля."""
        await callback_query.message.edit_text(
            text=i18n.register.car.scene.enter(),
            reply_markup=back_kb().as_markup(),
        )
        await self.wizard.update_data(previous_message=callback_query.message)

    @on.message(
        F.text.upper().regexp(LICENSE_PLATE_REGEX),
        after=After.goto(MenuOptions.MAIN_MENU_USER.scene),
    )
    async def input_license_plate_number(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Обрабатывает cообщение с текстом, который соответствует регулярному выражению LICENSE_PLATE_REGEX
        гос. номер автомобиля пользователя:
        - Проверяет уникальность номера и принадлежность пользователю.
        - Удаляет предыдущее сообщение бота при запуске через callback_query.
        - Создает новую запись о автомобиле или обновляет существующую.
        """
        data: dict = await self.wizard.get_data()
        previous_message: Optional[Message] = data.get("previous_message")

        if previous_message:
            await previous_message.delete()

        license_plate_number = message.text.upper()

        try:
            car = await repo.cars.check_unique_number(
                license_plate_number=license_plate_number
            )

            if car and car.user_id != user.id:
                await message.answer(
                    text=i18n.input.license.plate.number.used(
                        data=license_plate_number
                    )
                )
                return await self.wizard.retake()

            if not user.car:
                await repo.cars.create(
                    data=dict(license_plate_number=license_plate_number),
                    user=user,
                )
            else:
                await repo.cars.update(
                    obj=user.car,
                    update_data=dict(
                        license_plate_number=license_plate_number
                    ),
                )
            await message.answer(
                text=i18n.input.license.plate.number.success()
            )

        except Exception as e:
            logger.error(f"Error when saving car data: {e}")

    @on.message()
    async def input_invalid(self, message: Message, i18n: TranslatorRunner):
        """Обрабатывает некорректный ввод и перезапускает сцену."""
        await message.answer(text=i18n.input.data.invalid())
        await self.wizard.retake()
