from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner


from app.database.models import User
from app.bot.scenes.mixins import MenuScene
from app.database.repo.requests import RequestsRepo
from app.bot.keyboards.inline.user import profile_menu_kb


class ProfileScene(MenuScene, state="profile"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        await callback_query.message.edit_text(
            text=i18n.profile.menu.scene.enter(
                user=callback_query.from_user.full_name,
                license_plate_number=user.car.license_plate_number,
            ),
            reply_markup=profile_menu_kb(),
        )
