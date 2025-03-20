# src/schemas/register_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RegisterJsonSchema(BaseModel):
    name: str
    last_name: str
    role: str
    identification_number: str
    email: EmailStr
    permissions: str
    password: str  

    class Config:
        from_attributes = True  # Para compatibilidad con SQLAlchemy


