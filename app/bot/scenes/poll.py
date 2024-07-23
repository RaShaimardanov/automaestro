import asyncio
import os

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, FSInputFile
from fluentogram import TranslatorRunner

from app.bot.keyboards.inline.user import notifications_receive_kb
from app.bot.keyboards.inline.poll import launch_poll_kb, get_options_kb
from app.bot.utils.callback_data import PollCallback, AnswerCallback
from app.bot.utils.enums import MenuOptions
from app.core.logger import logger
from app.core.paths import IMAGES_DIR
from app.database.models import User, Question
from app.database.repo.requests import RequestsRepo


class PollScene(Scene, state="poll"):

    @on.callback_query.enter()
    async def callback_query_enter_poll(
        self,
        callback_query: CallbackQuery,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
        context: str = None,
    ):
        """Отправляет пользователю описание опроса и кнопку для запуска опроса."""
        if context:
            poll = await repo.polls.get_by_attribute(slug=context)

            if os.path.isfile(IMAGES_DIR / poll.image_name):
                # отправляем сообщение с изображением, если оно существует
                await callback_query.message.delete()
                await callback_query.message.answer_photo(
                    photo=FSInputFile(IMAGES_DIR / poll.image_name),
                    caption=poll.description,
                    reply_markup=launch_poll_kb(
                        poll_id=poll.id,
                        questions_quantity=len(poll.questions),
                    ),
                )
            else:
                await callback_query.message.edit_text(
                    text=poll.description,
                    reply_markup=launch_poll_kb(
                        poll_id=poll.id,
                        questions_quantity=len(poll.questions),
                    ),
                )
            return
        await self.wizard.goto(MenuOptions.MAIN_MENU_USER.scene)

    @on.callback_query(PollCallback.filter())
    async def launch_poll(
        self,
        callback_query: CallbackQuery,
        callback_data: PollCallback,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """Обрабатывает нажатие кнопки запуска опроса и отправляет первый вопрос."""
        question = await repo.questions.get_next_unanswered_question(
            user_id=user.id, poll_id=callback_data.poll_id
        )
        if question:
            await self._send_question(
                callback_query=callback_query,
                question=question,
                i18n=i18n,
                questions_quantity=callback_data.questions_quantity,
            )
            return
        await self.wizard.goto(MenuOptions.MAIN_MENU_USER.scene)

    @on.callback_query(AnswerCallback.filter())
    async def save_answer(
        self,
        callback_query: CallbackQuery,
        callback_data: AnswerCallback,
        user: User,
        repo: RequestsRepo,
        i18n: TranslatorRunner,
    ):
        """
        Обрабатывает нажатие кнопки с ответом и записывает ответ в базу данных.
        Проверяет наличие следующего вопроса в базе данных, если следующий вопрос существует, отправляет его пользователю.
        """
        try:
            # сохраняем пришедший ответ
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

        # запрашиваем новый вопрос
        question = await repo.questions.get_next_unanswered_question(
            user_id=user.id, poll_id=callback_data.poll_id
        )
        if question:
            # если вопрос есть, вызываем функцию отправки
            await self._send_question(
                callback_query=callback_query,
                question=question,
                i18n=i18n,
                questions_quantity=callback_data.questions_quantity,
                question_number=callback_data.question_number,
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
        """
        Выход из сцены при окончании опроса.
        Предлагает получить уведомление о готовности при наличии открытого визита,
        иначе завершает диалог.
        """

        await callback_query.message.answer(text=i18n.poll.scene.leave())
        await callback_query.message.delete()

        await asyncio.sleep(2)  # pause

        visit = await repo.visits.get_current_visit(user_id=user.id)

        if not visit:
            return await self.wizard.exit()

        await callback_query.message.answer(
            text=i18n.offer.receive.notifications(),
            reply_markup=notifications_receive_kb(visit_id=visit.id),
        )

    @staticmethod
    async def _send_question(
        callback_query: CallbackQuery,
        question: Question,
        i18n: TranslatorRunner,
        questions_quantity: int,
        question_number: int = 0,
    ):
        """Функция отправки вопроса"""
        try:
            question_number += 1

            await callback_query.message.delete()

            text = i18n.question.text(
                title=question.title,
                descripion=question.description,
                text_ask=question.text_ask,
                questions_quantity=questions_quantity,
                question_number=question_number,
            )

            if os.path.isfile(IMAGES_DIR / question.image_name):
                # отправляем сообщение с изображением, если оно существует
                await callback_query.message.answer_photo(
                    photo=FSInputFile(IMAGES_DIR / question.image_name),
                    caption=text,
                    reply_markup=get_options_kb(
                        question=question,
                        questions_quantity=questions_quantity,
                        question_number=question_number,
                    ),
                )

            else:
                # иначе, текстовое сообщение
                await callback_query.message.answer(
                    text=text,
                    reply_markup=get_options_kb(
                        question=question,
                        questions_quantity=questions_quantity,
                        question_number=question_number,
                    ),
                )

        except TelegramBadRequest as e:
            logger.error(
                f"Error while sending question: {question.id}. Exception: {e}"
            )

        except Exception as e:
            logger.error(
                f"Error while sending question: {question.id}. Exception: {e}"
            )
