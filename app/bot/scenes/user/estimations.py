from aiogram import F
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery, Message, Voice
from fluentogram import TranslatorRunner

from app.database.models import User
from app.database.repo.requests import RequestsRepo
from app.utils.speech_to_text import transcribe_voice
from app.bot.utils.callback_data import EstimationsCallback


class EstimationsScene(Scene, state="estimations"):

    @on.callback_query(EstimationsCallback.filter())
    async def estimation_callback(
        self,
        callback_query: CallbackQuery,
        callback_data: EstimationsCallback,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        message = await callback_query.message.edit_text(
            text=i18n.accept.estimation()
        )
        visit = await repo.visits.get(int(callback_data.visit_id))
        await self.wizard.update_data(visit_id=visit.id, message=message)
        await repo.visits.update(
            visit, update_data=dict(csat=callback_data.score)
        )

    @on.message(F.text, after=After.exit())
    async def input_comment(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
    ):
        await self._set_comment(text=message.text, repo=repo, user_id=user.id)

    @on.message(F.voice.as_("voice"))
    async def input_voice(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        voice: Voice,
    ):
        await self.wizard.exit()
        text = await transcribe_voice(
            bot=message.bot, voice=voice, user_id=user.id
        )
        await self._set_comment(text=text, repo=repo, user_id=user.id)

    @on.message.exit()
    async def scene_exit(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        await message.answer(text=i18n.visit.end())

    async def _set_comment(
        self,
        text: str,
        user_id: int,
        repo: RequestsRepo,
    ):
        data = await self.wizard.get_data()
        visit_id = data.get("visit_id")
        visit = await repo.visits.get(visit_id)

        if message := data.get("message"):
            await message.delete()

        if not visit:
            visit = await repo.visits.get_last_visit_by_user_id(
                user_id=user_id
            )
        await repo.visits.update(visit, update_data={"comment": text})
