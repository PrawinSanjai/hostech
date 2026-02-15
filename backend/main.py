from fastapi import FastAPI

from router import (
    user,
    admin,
    patient,
    receptionist
)

app = FastAPI(title="hosTech-Backend", docs_url="/docs", openapi_tags=["hosTech-Backend"])

@app.get("/")
def home():
    return "Hellow, World!"

app.include_router(user.router, prefix='/user', tags=["User"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(patient.router, prefix='/patient', tags=["Patient"])
app.include_router(receptionist.router, prefix='/receptionist', tags=["Receptionist"])
