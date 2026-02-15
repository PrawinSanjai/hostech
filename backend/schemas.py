from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class DoctorCreate(BaseModel):
    user_id: int
    specialization: str

class PatientCreate(BaseModel):
    user_id: int
    age: int
    gender: str

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_time: datetime

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str
    prescription: str
