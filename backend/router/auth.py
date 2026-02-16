from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import schemas
from services import auth

router = APIRouter()
auth_service = auth.AuthService()


@router.post("/register")
def register_user(user: schemas.UserRegister):
    if user.role.lower() != "patient":
        raise HTTPException(
            status_code=403,
            detail="Only patients can self-register"
        )
    return auth_service.register_user(user=user)

@router.post("/login")
def login(user_formdata: OAuth2PasswordRequestForm = Depends()):
    return auth_service.login(user=user_formdata)