from fastapi import APIRouter, Depends

from services import receptionist, auth
 
router = APIRouter()
receptionist_service = receptionist.ReceptionistService()


@router.get("/appointments")
def view_appointments(current_user = Depends(auth.require_role("receptionist"))):
    return receptionist_service.view_appointments()

@router.put("/update-status/{appointment_id}")
def update_status(appointment_id: int, status: str, current_user = Depends(auth.require_role("receptionist"))):
    return receptionist_service.update_status(appointment_id, status)
