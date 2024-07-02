from typing import Any

from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, FSInputFile
from fluentogram import TranslatorRunner


from app.core.logger import logger
from app.core.paths import IMAGES_DIR
from app.database.models import User, Question
from app.database.repo.requests import RequestsRepo
from app.bot.utils.callback_data import PollCallback, AnswerCallback
from app.bot.keyboards.inline.user import offer_receive_notifications
from app.bot.keyboards.inline.poll import launch_poll_kb, get_options_kb


class PollScene(Scene, state="poll"):
    @on.callback_query.enter()
    async def callback_query_enter_poll(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        context: Any,
    ):
        """Отправляет пользователю описание опроса и кнопку для запуска опроса."""
        poll = await repo.polls.get_by_attribute(slug=context)
        await callback_query.message.edit_text(
            text=poll.description, reply_markup=launch_poll_kb(poll_id=poll.id)
        )

    @on.callback_query(PollCallback.filter())
    async def launch_poll(
        self,
        callback_query: CallbackQuery,
        callback_data: PollCallback,
        user: User,
        repo: RequestsRepo,
    ):
        """Обрабатывает нажатие кнопки запуска опроса и отправляет первый вопрос."""
        question = await repo.questions.get_next_unanswered_question(
            user_id=user.id, poll_id=callback_data.poll_id
        )
        if question:
            await self._send_question(
                callback_query=callback_query, question=question
            )
            return
        await self.wizard.exit()

    @on.callback_query(AnswerCallback.filter())
    async def save_answer(
        self,
        callback_query: CallbackQuery,
        callback_data: AnswerCallback,
        user: User,
        repo: RequestsRepo,
    ):
        """
        Обрабатывает нажатие кнопки с ответом и записывает ответ в базу данных.
        Проверяет наличие следующего вопроса в базе данных, если следующий вопрос существует, отправляет его пользователю.
        """
        try:
            await repo.answers.create(
                data=dict(
                    option=callback_data.option,
                    question_id=callback_data.question_id,
                ),
                user=user,
            )
        except Exception as e:
            logger.error(
                f"Error saving answer: {callback_data}. Exception: {e}"
            )
        question = await repo.questions.get_next_unanswered_question(
            user_id=user.id, poll_id=callback_data.poll_id
        )
        if question:
            await self._send_question(
                callback_query=callback_query, question=question
            )
            return
        await self.wizard.leave()

    @on.callback_query.leave()
    async def scene_leave(
        self,
        callback_query: CallbackQuery,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """"""
        await callback_query.message.delete()
        await callback_query.message.answer(text=i18n.poll.scene.leave())
        visit = await repo.visits.get_current_visit(user_id=user.id)

        if not visit:
            return await self.wizard.exit()

        await callback_query.message.answer(
            text=i18n.offer.receive.notifications(),
            reply_markup=offer_receive_notifications(),
        )

    @staticmethod
    async def _send_question(
        callback_query: CallbackQuery, question: Question
    ):
        try:
            await callback_query.message.delete()
            if not question.image_name:
                await callback_query.message.answer(
                    text=question.text,
                    reply_markup=get_options_kb(question=question),
                )
                return
            await callback_query.message.answer_photo(
                photo=FSInputFile(IMAGES_DIR / question.image_name),
                caption=question.text,
                reply_markup=get_options_kb(question=question),
            )
        except Exception as e:
            logger.error(
                f"Error while sending question: {question}. Exception: {e}"
            )
