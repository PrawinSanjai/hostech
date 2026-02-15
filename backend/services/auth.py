from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import oauth2_scheme
import models
from database import db_session
from config import Configuration

config = Configuration()

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")


class AuthService:
    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data:dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
        except JWTError:
            raise credentials_exception

        with db_session() as db:
            user = db.query(models.User).filter(models.User.id == user_id).first()

            if user is None:
                raise credentials_exception

            return user
    
    def require_role(self, required_role: str):
        def role_checker(user: models.User = Depends(self.get_current_user)):
            if user.role != required_role:
                raise HTTPException(status_code=403, detail="Access denied")
            return user
        return role_checker
    
    def register_user(self, user: dict):
        hashed_pw = self.hash_password(user.password)
        with db_session() as db:
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

    def login(self, user: dict):
        with db_session() as db:
            db_user = db.query(models.User).filter(models.User.email == user.email).first()

            if not db_user or not self.verify_password(user.password, db_user.hashed_password):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            access_token = self.create_access_token(
                data={"user_id": db_user.id, "role": db_user.role}
            )
            return {"access_token": access_token, "token_type": "bearer"}
