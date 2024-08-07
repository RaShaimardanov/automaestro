from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base


class Car(Base):
    brand: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    license_plate_number: Mapped[str] = mapped_column(
        String(9), unique=True, comment="Гос. номер", nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(  # type: ignore
        "User", back_populates="car", lazy="selectin"
    )

    def __str__(self):
        return self.license_plate_number
