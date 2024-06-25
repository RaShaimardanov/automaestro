from aiogram import F
from aiogram.types import Message
from aiogram.fsm.scene import on, Scene
from fluentogram import TranslatorRunner

from app.database.models import User
from app.bot.scenes.user import MainMenuUserScene
from app.core.constants import LICENSE_PLATE_REGEX
from app.database.repo.requests import RequestsRepo


class RegisterCarScene(Scene, state="register_car"):
    """Сцена для регистрации гос. номера автомобиля"""

    @on.message.enter()
    async def on_enter_register_car(
        self,
        message: Message,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает вход в сцену регистрации гос. номера автомобиля."""
        await message.answer(text=i18n.register.car.scene.enter())

    @on.message(F.text.upper().regexp(LICENSE_PLATE_REGEX))
    async def input_license_plate_number(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает ввод номера автомобиля и проверяет его уникальность."""
        license_plate_number = message.text.upper()

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

        await repo.cars.create(
            data=dict(license_plate_number=license_plate_number), user=user
        )
        await message.answer(text=i18n.input.license.plate.number.success())
        await self.wizard.goto(MainMenuUserScene)

    @on.message()
    async def input_skip(self, message: Message, i18n: TranslatorRunner):
        """Обрабатывает некорректный ввод и перезапускает сцену."""
        await message.answer(text=i18n.input.data.invalid())
        await self.wizard.retake()
