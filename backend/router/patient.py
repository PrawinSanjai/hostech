from fastapi import APIRouter

import schemas
from services import patient

router = APIRouter()
patient_service = patient.PatientService()


@router.post("/book")
def book_appointment(app: schemas.AppointmentCreate):
    return patient_service.book_appointment(app)

@router.get("/records/{patient_id}")
def view_records(patient_id: int):
    return patient_service.view_records(patient_id)