from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    specialization: Mapped[str] = mapped_column(String(100))

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
    )
