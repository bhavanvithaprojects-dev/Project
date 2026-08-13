from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def has_overlapping_appointment(
    db: Session,
    doctor_id: int,
    appointment_start: datetime,
    appointment_end: datetime,
):
    appointment = db.scalar(
        select(Appointment).where(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_start < appointment_end,
            Appointment.appointment_end > appointment_start,
        )
    )

    if appointment:
        return True

    return False
