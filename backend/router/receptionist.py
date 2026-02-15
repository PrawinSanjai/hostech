from fastapi import APIRouter

from services import receptionist
 
router = APIRouter()
receptionist_service = receptionist.ReceptionistService()


@router.get("/appointments")
def view_appointments():
    return receptionist_service.view_appointments()

@router.put("/update-status/{appointment_id}")
def update_status(appointment_id: int, status: str):
    return receptionist_service.update_status(appointment_id, status)
