import models
from database import db_session

class DoctorService():
    def get_patients(doctor_id: int):
        with db_session() as db:
            return db.query(models.Appointment).filter(
                models.Appointment.doctor_id == doctor_id
            ).all()


    def add_record(record: dict):
        with db_session() as db:
            new_record = models.MedicalRecord(**record.dict())
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return new_record