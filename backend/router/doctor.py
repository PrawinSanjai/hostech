from fastapi import APIRouter, Depends

import schemas
from services import doctor, auth

router = APIRouter()
doctor_service = doctor.DoctorService()

@router.get("/patients/{doctor_id}")
def get_patients(doctor_id: int, current_user = Depends(auth.require_role("admin"))):
    return doctor_service.get_patients(doctor_id)

@router.post("/add-record")
def add_record(record: schemas.MedicalRecordCreate, current_user = Depends(auth.require_role("admin"))):
    return doctor_service.add_record(record)