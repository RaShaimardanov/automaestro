from aiogram.fsm.scene import on, After
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.user import notifications_setting_kb
from app.bot.scenes.mixins import MenuScene
from app.bot.utils.callback_data import NotificationsCallback
from app.bot.utils.enums import MenuOptions
from app.core.logger import logger
from app.database.models import User
from app.database.repo.requests import RequestsRepo


class NotificationsScene(MenuScene, state="notifications"):
    """Сцена настройки уведомлений"""

    @on.callback_query.enter()
    async def on_enter(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Отправляет сообщение с текущим состоянием настройки уведомлений и клавиатурой для изменения состояния.
        """
        try:
            visit = await repo.visits.get_current_visit(user_id=user.id)
            await callback_query.message.edit_text(
                text=i18n.receive.notification.ask(
                    position=visit.notify_ready
                ),
                reply_markup=notifications_setting_kb(
                    position=visit.notify_ready, visit_id=visit.id
                ),
            )
        except Exception as e:
            logger.exception(
                f"Error send message notifications settings scene {user.telegram_id}: {e}"
            )

    @on.callback_query(
        NotificationsCallback.filter(),
        after=After.goto(MenuOptions.MAIN_MENU_USER.scene),
    )
    async def save_position_notifications(
        self,
        callback_query: CallbackQuery,
        callback_data: NotificationsCallback,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Принимает нажатие кнопки настройки уведомлений и сохраняет.
        После выполнения отправляет пользователя в главное меню.
        """
        try:
            visit = await repo.visits.get(int(callback_data.visit_id))

            await repo.visits.update(
                visit, dict(notify_ready=bool(callback_data.position))
            )

            await callback_query.answer(
                text=i18n.switch.notifications(select=callback_data.position),
                show_alert=True,
            )

        except Exception as e:
            logger.exception(
                f"Error saving notifications settings {user.telegram_id}: {e}"
            )
