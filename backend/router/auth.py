from fastapi import APIRouter

import schemas
from services import auth

router = APIRouter()
auth_service = auth.AuthService()


@router.post("/register")
def register_user(user: schemas.UserRegister):
    return auth_service.register_user(user=user)

@router.post("/login")
def login(user: schemas.UserLogin):
    return auth_service.login(user=user)