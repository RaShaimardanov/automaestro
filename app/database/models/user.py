from sqlalchemy.orm import Mapped, relationship

from app.database.models.base import Base
from app.database.models.car import Car
from app.database.models.mixins import UserMixin


class User(UserMixin, Base):
    car: Mapped[Car] = relationship(
        Car, back_populates="user", cascade="delete", lazy="selectin"
    )


class Employee(UserMixin, Base):
    pass
