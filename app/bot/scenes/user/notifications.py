from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner


from app.database.models import User
from app.bot.utils.enums import MenuOptions
from app.bot.scenes.mixins import BackScene
from app.database.repo.requests import RequestsRepo
from app.bot.utils.callback_data import NotificationsCallback
from app.bot.keyboards.inline.user import configuration_notifications


class NotificationsScene(BackScene, state="notifications"):
    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visit = await repo.visits.get_current_visit(user_id=user.id)
        await callback_query.message.edit_text(
            text=i18n.receive.notification.ask(position=visit.notify_ready),
            reply_markup=configuration_notifications(visit.notify_ready),
        )

    @on.callback_query(NotificationsCallback.filter())
    async def save_position_notifications(
        self,
        callback_query: CallbackQuery,
        callback_data: NotificationsCallback,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        visit = await repo.visits.get_current_visit(user_id=user.id)
        await repo.visits.update(
            visit, dict(notify_ready=callback_data.position)
        )
        await self.wizard.goto(MenuOptions.MAIN_MENU.scene)
