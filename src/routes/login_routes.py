# src/routes/login_routes.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from ..models.login import User, Login, authenticate_user, register_login
from ..schemas.login_schema import LoginRequest, LoginResponse
from ..database import get_db

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Endpoint para loguear un user
@router.post("/login")
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Autenticar al usuario
        user = authenticate_user(login_request.email, login_request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Correo electrónico o contraseña incorrectos")

        # Registrar el inicio de sesión
        new_login = register_login(user.id)
        db.add(new_login)
        db.commit()

        return {"message": "Inicio de sesión exitoso", "user_id": user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para obtener todos los inicios de sesión de un usuario
@router.get("/logins/{user_id}", response_model=List[LoginResponse])
async def get_user_logins(user_id: str, db: Session = Depends(get_db)):
    try:
        logins = db.query(Login).filter(Login.id_user == user_id).all()
        return logins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))