from typing import Optional, Dict

from aiogram.fsm.scene import on
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner

from app.bot.utils.callback_data import EstimationsCallback
from app.database.models import User
from app.bot.scenes.mixins import MenuScene
from app.database.repo.requests import RequestsRepo
from app.bot.keyboards.inline.user import main_menu_user_kb


class MainMenuUserScene(MenuScene, state="main_menu_user"):
    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        context = await self._create_context(user, repo)
        # статус автомобиля
        if any(context.values()):
            message = await message.answer(
                text=i18n.main.menu.user(),
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
        message: Optional[Message] = None,
    ):
        context = await self._create_context(user, repo)
        if any(context.values()):
            if message:
                await message.answer(
                    text=i18n.main.menu.user(),
                    reply_markup=main_menu_user_kb(
                        context=context,
                    ),
                )
                return
            message = await callback_query.message.edit_text(
                text=i18n.main.menu.user(),
                reply_markup=main_menu_user_kb(
                    context=context,
                ),
            )
            await self.wizard.update_data(message=message)

    @staticmethod
    async def _create_context(
        user: User,
        repo: RequestsRepo,
    ) -> Dict[str, str]:
        poll = await repo.polls.get_polls_with_unanswered_questions(
            user_id=user.id
        )
        visit = await repo.visits.get_current_visit(user_id=user.id)
        return {
            "POLL": getattr(poll, "slug", None),
            "PROFILE": getattr(visit, "user_id", None),
            "VISIT_CARD": getattr(visit, "employee_id", None),
        }
