# src/schemas/login_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: str
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    
# Modelo de respuesta para el inicio de sesiónclass LoginResponse(BaseModel):
    message: str
    user_id: str
    access_token: str | None = None
    token_type: str | None = None
# Agregar esto a login_schema.py
class UserLoginSchema(BaseModel):
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

class Token(BaseModel):
    access_token: str
    token_type: str