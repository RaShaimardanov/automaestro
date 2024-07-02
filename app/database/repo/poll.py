from typing import Optional

from sqlalchemy import select, and_, not_
from sqlalchemy.orm import joinedload

from app.database.repo.base import BaseRepo
from app.database.models import Poll, Question, Answer


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

    async def get_next_poll(self, user_id: int) -> Optional[Poll]:
        stmt = (
            select(Poll)
            .join(Poll.questions)
            .outerjoin(
                Answer,
                and_(
                    Answer.question_id == Question.id,
                    Answer.user_id == user_id,
                    Answer.id.is_(None),
                ),
            )
            .distinct()
            .order_by(Poll.id)
        )
        result = await self.session.execute(stmt)
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
    pass
