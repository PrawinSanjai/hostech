from fastapi import APIRouter, Depends

import schemas
from services import patient, auth

router = APIRouter()
patient_service = patient.PatientService()


@router.post("/book")
def book_appointment(app: schemas.AppointmentCreate, current_user = Depends(auth.require_role("patient"))):
    return patient_service.book_appointment(app)

@router.get("/records/{patient_id}")
def view_records(patient_id: int, current_user = Depends(auth.require_role("patient"))):
    return patient_service.view_records(patient_id)