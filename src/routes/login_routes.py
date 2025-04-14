# src/routes/login_routes.py
from typing import List
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from src.models.login import authenticate_user, Login, register_login
from src.schemas.login_schema import LoginRequest, LoginResponse
from src.database import get_db
import jwt
from src.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from pydantic import BaseModel
from src.schemas.login_schema import LoginRequest, LoginResponse, Token 
from src.models.register import User
from sqlalchemy import Column, String

router = APIRouter()

# Configuración JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
class LoginRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint para loguear un user (versión actualizada con JWT)
async def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    # Verificar que se proporcionó email
    if not login_data.email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Autenticar usuario
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Registrar el login (solo información esencial)
    login_record = Login(
        id_user=str(user.id),
        email=user.email
    )
    db.add(login_record)
    db.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "email": user.email,
            "user_id": str(user.id)
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=Token)
async def login_for_access_token_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)  # ✅ Asegurar que 'db' sea una sesión SQLAlchemy
):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

    