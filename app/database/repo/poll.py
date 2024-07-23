from typing import Optional, List

from sqlalchemy import select, and_, not_
from sqlalchemy.orm import joinedload, selectinload

from app.database.repo.base import BaseRepo
from app.database.models import Poll, Question, Answer
from app.utils.enums import PollType


class PollRepo(BaseRepo):
    async def get_polls_with_unanswered_questions(
        self, user_id: int
    ) -> Optional[Poll]:
        answered_subquery = (
            select(Answer.question_id)
            .where(user_id == Answer.user_id)
            .subquery()
        )

        result = await self.session.execute(
            select(Poll)
            .join(Poll.questions)
            .where(Question.id.not_in(select(answered_subquery)))
            .order_by(Poll.id)
            .distinct()
        )

        poll = result.scalars().first()
        return poll

    async def get_next_poll(self, user_id: int, poll_type) -> Optional[Poll]:
        answered_subquery = (
            select(Answer.question_id)
            .where(user_id == Answer.user_id)
            .subquery()
        )

        result = await self.session.execute(
            select(Poll)
            .where(Poll.poll_type == poll_type)
            .join(Poll.questions)
            .where(Question.id.not_in(select(answered_subquery)))
            .order_by(Poll.id)
            .distinct()
        )

        poll = result.scalars().first()
        return poll


class QuestionRepo(BaseRepo):
    async def get_next_unanswered_question(self, user_id: int, poll_id: int):
        subquery = (
            select(Answer)
            .where(
                and_(
                    Answer.question_id == Question.id,
                    Answer.user_id == user_id,
                )
            )
            .exists()
        )

        stmt = (
            select(Question)
            .where(
                and_(
                    Question.poll_id == poll_id,
                    not_(subquery),
                )
            )
            .order_by(Question.id)
        )

        result = await self.session.execute(stmt)
        question = result.scalars().first()
        return question


class OptionRepo(BaseRepo):
    pass


class AnswerRepo(BaseRepo):
    async def get_answers_by_question_id(self, question_id: int):
        stmt = select(Answer).where(question_id == Answer.question_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_answers_by_poll_id(self, poll_id: int):
        result = await self.session.execute(
            select(Answer)
            .join(Question, Answer.question_id == Question.id)
            .join(Poll, Question.poll_id == Poll.id)
            .where(poll_id == Poll.id)
        )
        answers = result.scalars().all()
        return answers
