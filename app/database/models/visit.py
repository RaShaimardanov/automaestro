from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base
from app.database.models.mixins import TimestampMixin
from app.database.models.user import User
from app.utils.enums import OrderStatus


class Visit(Base, TimestampMixin):
    status: Mapped[ENUM] = mapped_column(
        ENUM(OrderStatus),
        nullable=False,
        default=OrderStatus.SERVICE,
    )
    close_date = mapped_column(TIMESTAMP, nullable=True)
    csat: Mapped[int] = mapped_column(Integer, nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    notify_ready: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL")
    )
    user: Mapped[User] = relationship(
        User,
        backref="user",
        lazy="selectin",
    )
