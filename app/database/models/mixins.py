from datetime import datetime

from sqlalchemy import BIGINT, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )


class UserMixin(TimestampMixin):
    __abstract__ = True

    telegram_id: Mapped[int] = mapped_column(
        BIGINT, unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(12), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)
