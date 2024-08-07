from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base
from app.utils.enums import OptionsType, PollType


class Poll(Base):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_name: Mapped[str] = mapped_column(String, nullable=True)
    poll_type: Mapped[ENUM] = mapped_column(
        ENUM(PollType),
        nullable=False,
        default=PollType.CLIENT,
    )
    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        backref="questions",
        cascade="delete",
        lazy="selectin",
        order_by="Question.id",
    )


class Question(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    text_ask: Mapped[str] = mapped_column(String, nullable=False)
    image_name: Mapped[str] = mapped_column(String, nullable=True)
    poll_id: Mapped[int] = mapped_column(
        ForeignKey("polls.id"), nullable=False
    )
    options_type: Mapped[ENUM] = mapped_column(
        ENUM(OptionsType),
        nullable=False,
        default=OptionsType.SMILE,
    )
    options_list: Mapped[Optional[list["Option"]]] = relationship(
        "Option",
        backref="options_list",
        uselist=True,
        lazy="selectin",
        cascade="delete",
    )

    @hybrid_property
    def options(self):
        if self.options_type.value:
            return [option for option in self.options_type.value]
        return self.options_list


class Option(Base):
    value: Mapped[str] = mapped_column(String, nullable=False)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), nullable=False
    )

    def __str__(self):
        return self.value


class Answer(Base):
    option: Mapped[str] = mapped_column(String, nullable=False)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
