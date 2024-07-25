from typing import Dict

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.scene import on
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.user import main_menu_user_kb
from app.bot.scenes.mixins import MenuScene
from app.core.logger import logger
from app.database.models import User
from app.database.repo.requests import RequestsRepo
from app.utils.enums import PollType


class MainMenuUserScene(MenuScene, state="main_menu_user"):
    """Сцена отправки сообщения главного меню"""

    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        context = await self._create_context(user, repo)
        text = await self._generate_text(context, i18n)

        if any(context.values()):
            message = await message.answer(
                text=text,
                reply_markup=main_menu_user_kb(context=context),
            )
            await self.wizard.update_data(message=message)
        else:
            await self.wizard.exit()

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        context = await self._create_context(user, repo)
        text = await self._generate_text(context, i18n)

        try:
            if any(context.values()):
                message = await callback_query.message.edit_text(
                    text=text,
                    reply_markup=main_menu_user_kb(
                        context=context,
                    ),
                )
                await self.wizard.update_data(message=message)

        except TelegramBadRequest as e:
            # если предыдущее сообщение невозможно изменить
            if "message is not modified" in str(e):
                await callback_query.message.delete()
                message = await callback_query.bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    reply_markup=main_menu_user_kb(context=context),
                )
                await self.wizard.update_data(message=message)
            else:
                logger.error(f"Error menu message {user.telegram_id}: {e}")

        except Exception as e:
            logger.error(f"Error menu message {user.telegram_id}: {e}")

    @staticmethod
    async def _create_context(
        user: User,
        repo: RequestsRepo,
    ) -> Dict[str, str]:
        poll = await repo.polls.get_next_poll(
            user_id=user.id, poll_type=PollType.CLIENT
        )
        visit = await repo.visits.get_current_visit(user_id=user.id)
        return {
            "POLL": getattr(poll, "slug", None),
            "PROFILE_USER": getattr(visit, "user_id", None),
            "VISIT_CARD": getattr(visit, "employee_id", None),
        }

    @staticmethod
    async def _generate_text(context, i18n):
        poll = context.get("POLL")
        visit = context.get("VISIT_CARD")
        return i18n.user.main.menu.scene(poll=bool(poll), visit=bool(visit))
