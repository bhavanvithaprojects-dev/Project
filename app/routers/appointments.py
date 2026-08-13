from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patients import Patient
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
)
from app.services.appointments import has_overlapping_appointment

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    if appointment.appointment_start >= appointment.appointment_end:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Appointment end must be after appointment start",
        )

    patient = db.get(Patient, appointment.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found",
        )

    doctor = db.get(Doctor, appointment.doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    overlap = has_overlapping_appointment(
        db,
        appointment.doctor_id,
        appointment.appointment_start,
        appointment.appointment_end,
    )

    if overlap:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already has an overlapping appointment",
        )

    new_appointment = Appointment(**appointment.model_dump())

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    appointment = db.get(Appointment, appointment_id)

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    return appointment
