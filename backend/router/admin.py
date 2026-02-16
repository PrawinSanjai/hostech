from fastapi import APIRouter, Depends

import models, schemas
from services import admin, auth

router = APIRouter()
admin_service = admin.AdminService()


@router.post("/add-doctor")
def add_doctor(doctor: schemas.DoctorCreate, current_user = Depends(auth.require_role("admin"))):
    return admin_service.add_doctor(doctor)

@router.post("/add-receptionist")
def add_receptionist(user: schemas.UserCreate, current_user = Depends(auth.require_role("admin"))):
    return admin_service.add_receptionist(user)

@router.get("/records")
def view_all_records(current_user = Depends(auth.require_role("admin"))):
    return admin_service.view_all_records()