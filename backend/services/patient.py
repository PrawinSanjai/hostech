import models
from database import db_session


class PatientService:
    def book_appointment(app: dict):
        with db_session() as db:
            appointment = models.Appointment(**app.model_dump())
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            return appointment

    def view_records(patient_id: int):
        with db_session() as db:
            records = db.query(models.MedicalRecord).filter(
                models.MedicalRecord.patient_id == patient_id
            ).all()
            return records