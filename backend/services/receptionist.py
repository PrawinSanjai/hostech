from database import db_session
import models

class ReceptionistService:
    def view_appointments():
        with db_session() as db:
            return db.query(models.Appointment).all()

    def update_status(appointment_id: int, status: str):
        with db_session() as db:
            appointment = db.query(models.Appointment).get(appointment_id)
            appointment.status = status
            db.commit()
            return appointment