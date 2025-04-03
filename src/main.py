# src/main.py
from http.client import HTTPException
import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .database import SessionSql, init_db, get_db
from src.models import pqrsf
from src.models.register import User, UserJsonSchema
from src.routes import login_routes, forgot_password_routes, pqrsf_routes, register_routes  
from fastapi.middleware.cors import CORSMiddleware
from .business_logic.forgot_password_logic import request_password_reset
from .schemas.forgot_password_schemas import ForgotPasswordRequest
from .config import DATABASE_URL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    from src.database import init_db
    print("Creando base de datos...")
    init_db()
    print("Base de datos lista.")

from src.routes import pqrsf_routes, register_routes, login_routes, forgot_password_routes

app.include_router(pqrsf_routes.router)
app.include_router(register_routes.router)
app.include_router(login_routes.router)
app.include_router(forgot_password_routes.router)

init_db ()

@app.get("/")
def read_root():
    return {"message": "Sistema DIAN - Backend"}

PDF_PATH = r"C:\Users\DIACA\PROJECTS\ACCOUNTING_SYSTEM\demo-dian\public\assets\Guía Completa del Sistema de Contabilidad DIAN-Colombia.pdf"

@app.get("/descargar-guia")
async def descargar_guia():
    if not os.path.exists(PDF_PATH):
        raise HTTPException(
            status_code=404,
            detail="El archivo de la guía no se encuentra disponible temporalmente"
        )
    
    return FileResponse(
        path=PDF_PATH,
        filename="Guia_Contable_DIAN.pdf",
        media_type="application/pdf"
    )