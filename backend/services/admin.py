import models
from database import db_session

class AdminService:
    def add_doctor(doctor: dict):
        with db_session() as db:
            new_doctor = models.Doctor(**doctor.model_dump())
            db.add(new_doctor)
            db.commit()
            db.refresh(new_doctor)
            return new_doctor
    
    def add_receptionist(user: dict):
        with db_session() as db:
            user.role = "receptionist"
            new_user = models.User(**user.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
    
    def view_all_records():
        with db_session() as db:
            records = db.query(models.MedicalRecord).all()
            return records