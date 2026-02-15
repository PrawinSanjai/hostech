from fastapi import APIRouter

import schemas
from services import doctor

router = APIRouter()
doctor_service = doctor.DoctorService()

@router.get("/patients/{doctor_id}")
def get_patients(doctor_id: int):
    return doctor_service.get_patients(doctor_id)

@router.post("/add-record")
def add_record(record: schemas.MedicalRecordCreate):
    return doctor_service.add_record(record)
