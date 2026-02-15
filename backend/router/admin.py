from fastapi import APIRouter

import models, schemas
from services import admin

router = APIRouter()
admin_service = admin.AdminService()


@router.post("/add-doctor")
def add_doctor(doctor: schemas.DoctorCreate):
    return admin_service.add_doctor(doctor)

@router.post("/add-receptionist")
def add_receptionist(user: schemas.UserCreate):
    return admin_service.add_receptionist(user)

@router.get("/records")
def view_all_records():
    return admin_service.view_all_records()