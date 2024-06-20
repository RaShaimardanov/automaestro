from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models import Base


class Car(Base):
    brand: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    license_plate_number: Mapped[str] = mapped_column(
        String(9), unique=True, comment="Гос. номер", nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
