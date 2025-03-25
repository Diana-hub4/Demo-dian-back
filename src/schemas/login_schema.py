# src/schemas/login_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

# Modelo de solicitud para crear un usuario
class UserRequest(BaseModel):
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

# Modelo de respuesta para el usuario
class UserResponse(BaseModel):
    id: str = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Correo electrónico del usuario")

# Modelo de solicitud para registrar un inicio de sesión
class LoginRequest(BaseModel):
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

# Modelo de respuesta para el inicio de sesión
class LoginResponse(BaseModel):
    id: str = Field(..., description="ID único del inicio de sesión")
    id_user: str = Field(..., description="ID del usuario que inició sesión")
    login_date: datetime = Field(..., description="Fecha y hora del inicio de sesión")