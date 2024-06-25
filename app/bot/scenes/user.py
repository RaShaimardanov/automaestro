from aiogram.types import Message
from aiogram.fsm.scene import Scene, on
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.user import main_menu_profile
from app.database.models import User


class MainMenuUserScene(
    Scene,
    state="main_menu_user",
):
    @on.message.enter()
    async def on_enter(
        self, message: Message, user: User, i18n: TranslatorRunner
    ):
        await message.answer(
            text=i18n.main.menu.user(),
            reply_markup=main_menu_profile(slug_poll="yes"),
        )
