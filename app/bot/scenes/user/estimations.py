import asyncio

from aiogram import F
from aiogram.fsm.scene import Scene, on, After
from aiogram.types import CallbackQuery, Message, Voice
from celery.result import AsyncResult
from fluentogram import TranslatorRunner

from app.database.models import User
from app.database.repo.requests import RequestsRepo
from app.services.tasks.messages import transcribe_voice_task
from app.bot.utils.callback_data import EstimationsCallback
from app.utils.speech_to_text import download_and_convert_voice


class EstimationsScene(Scene, state="estimations"):
    """Сцена оценки визита и сохранения коментария к визиту"""

    @on.callback_query(EstimationsCallback.filter())
    async def estimation_callback(
        self,
        callback_query: CallbackQuery,
        callback_data: EstimationsCallback,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """Принимает callback_query с оценкой и сохраняет сохрает данные в визит"""
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
        """Принимает текстовое сообщение и сохраняет в поле комментария визита"""
        await self._set_comment(text=message.text, repo=repo, user_id=user.id)

    @on.message(F.voice.as_("voice"))
    async def input_voice(
        self,
        message: Message,
        user: User,
        repo: RequestsRepo,
        voice: Voice,
    ):
        """Принимает голосовое сообщение, переводит его в текст и сохраняет в поле комментария визита"""
        await self.wizard.exit()

        # сохраняем голосовое и получаем путь
        voice_path = await download_and_convert_voice(
            voice_file_id=voice.file_id, user_id=user.id
        )

        # запускаем задачу перевода голосового сообщения в текст
        task = transcribe_voice_task.delay(voice_path=voice_path)
        result = AsyncResult(task.id)

        # ожидаем завершения задачи
        while not result.ready():
            await asyncio.sleep(1)

        transcribed_text = result.result

        # сохраняем результат
        await self._set_comment(
            text=transcribed_text, repo=repo, user_id=user.id
        )

    @on.message.exit()
    async def scene_exit(
        self,
        message: Message,
        i18n: TranslatorRunner,
    ):
        """Отправляет последнее сообщение"""
        await message.answer(text=i18n.visit.end())

    async def _set_comment(
        self,
        text: str,
        user_id: int,
        repo: RequestsRepo,
    ):
        """Функция сохранения текста сообщения"""
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
