from aiogram.fsm.scene import on
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner


from app.database.models import User
from app.bot.scenes.mixins import MenuScene
from app.database.repo.requests import RequestsRepo
from app.bot.keyboards.inline.user import main_menu_user_kb


class MainMenuUserScene(
    MenuScene, state="main_menu_user", reset_history_on_enter=True
):
    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        poll = await repo.polls.get_polls_with_unanswered_questions(
            user_id=user.id
        )

        await message.answer(
            text=i18n.main.menu.user(),
            reply_markup=main_menu_user_kb(
                context=poll.slug if poll else None,
            ),
        )

    @on.callback_query.enter()
    async def on_enter_callback(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        poll = await repo.polls.get_polls_with_unanswered_questions(
            user_id=user.id
        )
        await callback_query.message.edit_text(
            text=i18n.main.menu.user(),
            reply_markup=main_menu_user_kb(
                context=poll.slug if poll else None,
            ),
        )
