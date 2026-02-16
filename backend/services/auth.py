from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

import models
from database import db_session
from config import Configuration

config = Configuration()

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=401,
    detail="Invalid credentials"
)


class AuthService:
    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def register_user(self, user):
        with db_session() as db:
            existing_user = db.query(models.User).filter(models.User.email == user.email).first()

            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")

            hashed_pw = self.hash_password(user.password)

            new_user = models.User(
                name=user.name,
                email=user.email,
                hashed_password=hashed_pw,
                role=user.role
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        return {"message": "User created successfully"}

    def login(self, user):
        with db_session() as db:
            db_user = db.query(models.User).filter(
                models.User.email == user.username
            ).first()

            if not db_user or not self.verify_password(
                user.password,
                db_user.hashed_password
            ):
                raise CREDENTIALS_EXCEPTION

            access_token = self.create_access_token(
                data={"user_id": db_user.id, "role": db_user.role}
            )

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    with db_session() as db:
        user = db.query(models.User).filter(
            models.User.id == user_id
        ).first()

        if not user:
            raise CREDENTIALS_EXCEPTION

        return user


def require_role(required_role: str):
    def role_checker(user: models.User = Depends(get_current_user)):
        if user.role.lower() == "admin":
            return user

        if user.role.lower() != required_role.lower():
            raise HTTPException(status_code=403, detail="Access denied")

        return user

    return role_checker


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != config.HOSTECH_API_KEY:
        raise CREDENTIALS_EXCEPTION
    return api_key
