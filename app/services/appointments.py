from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def has_overlapping_appointment(
    db: Session,
    doctor_id: int,
    appointment_start: datetime,
    appointment_end: datetime,
) -> bool:
    statement = select(Appointment).where(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_start < appointment_end,
        Appointment.appointment_end > appointment_start,
    )

    return db.scalar(statement) is not None
