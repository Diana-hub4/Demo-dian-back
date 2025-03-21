# src/routes/login_routes.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from ..models.login import User, Login, authenticate_user, register_login
from ..schemas.login_schema import UserRequest, UserResponse, LoginRequest, LoginResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo usuario
@router.post("/register", response_model=UserResponse)
async def create_user(user: UserRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

        # Crear un nuevo usuario
        new_user = User(email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para autenticar un usuario
@router.post("/login", response_model=UserResponse)
async def login_user(email: str, password: str, db: SessionLocal = Depends(get_db)):
    try:
        # Autenticar al usuario
        user = authenticate_user(email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Correo electrónico o contraseña incorrectos")

        # Registrar el inicio de sesión
        new_login = register_login(user.id)
        db.add(new_login)
        db.commit()

        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los inicios de sesión de un usuario
@router.get("/logins/{user_id}", response_model=List[LoginResponse])
async def get_user_logins(user_id: str, db: SessionLocal = Depends(get_db)):
    try:
        logins = db.query(Login).filter(Login.id_user == user_id).all()
        return logins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))