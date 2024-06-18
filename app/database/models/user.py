from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.database.models.base import Base
from app.database.models.mixins import UserMixin


class User(UserMixin, Base):
    pass


class Employee(UserMixin, Base):
    pass
