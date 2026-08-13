from fastapi import FastAPI

from app.routers.appointments import router as appointments_router
from app.routers.doctors import router as doctors_router
from app.routers.patients import router as patients_router

app = FastAPI(
    title="Hospital Appointment Management API",
    version="1.0.0",
)


app.include_router(patients_router)
app.include_router(doctors_router)
app.include_router(appointments_router)


@app.get("/health")
def health():
    return {"status": "ok"}
