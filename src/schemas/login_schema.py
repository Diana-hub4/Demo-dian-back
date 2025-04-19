# src/schemas/login_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from marshmallow import Schema, fields



# Modelo de solicitud para crear un usuario
class UserRequest(BaseModel):
    email: str = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")

# Modelo de respuesta para el usuario
class UserResponse(BaseModel):
    id: str = Field(..., description="ID único del usuario")
    email: str = Field(..., description="Correo electrónico del usuario")

# Modelo de solicitud para registrar un inicio de sesión
class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(..., description="Tipo de token")
    role: str = Field(..., description="Rol del usuario")
    user_id: str = Field(..., description="ID del usuario")
    message: str = Field(..., description="Mensaje de estado")
    
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
    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(..., description="Tipo de token")
class UserSchema(Schema):
    id = fields.Str()
    email = fields.Str()
    password_hash = fields.Str()

class LoginSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    email = fields.Str()
    name = fields.Str()
    identification = fields.Str()
    login_date = fields.DateTime()