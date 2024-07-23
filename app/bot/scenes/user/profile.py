from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from app.bot.utils.enums import MenuOptions
from app.database.models import User
from app.bot.scenes.mixins import MenuScene
from app.database.repo.requests import RequestsRepo
from app.bot.keyboards.inline.user import profile_menu_kb


class ProfileScene(MenuScene, state="profile_user"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visit = await repo.visits.get_last_visit_by_user_id(user_id=user.id)

        if not user.car:
            await self.wizard.goto(MenuOptions.REGISTER.scene)
            return

        await callback_query.message.edit_text(
            text=i18n.user.profile.menu.scene(
                user=callback_query.from_user.full_name,
                license_plate_number=user.car.license_plate_number,
                status=visit.status.name,
            ),
            reply_markup=profile_menu_kb(),
        )
