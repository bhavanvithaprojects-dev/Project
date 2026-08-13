from fastapi import FastAPI

from app.routers import appointments, doctors, patients

app = FastAPI(title="Hospital Appointment API")

app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
