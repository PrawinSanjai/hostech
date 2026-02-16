from fastapi import FastAPI, Depends

from router import (
    auth,
    user,
    admin,
    patient,
    receptionist,
    doctor
)

app = FastAPI(title="hosTech-Backend", docs_url="/docs")


@app.get("/")
def home():
    return "Hellow, World!"

app.include_router(auth.router, tags=["Auth"])
app.include_router(user.router, prefix='/user', tags=["User"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(patient.router, prefix='/patient', tags=["Patient"])
app.include_router(receptionist.router, prefix='/receptionist', tags=["Receptionist"])
app.include_router(doctor.router, prefix='/doctor', tags=["Doctor"])