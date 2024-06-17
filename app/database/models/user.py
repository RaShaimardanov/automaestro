from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.database.models.base import Base
from app.database.models.mixins import UserMixin


class User(UserMixin, Base):
    first_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(12), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)


class Employee(UserMixin, Base):
    pass
