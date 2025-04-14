# src/schemas/register_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


class UserJsonSchema(BaseModel):
    first_name: str  
    last_name: str
    role: str
    identification_number: str
    email: EmailStr
    permissions: str
    password: str  
    status: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Juan",
                "last_name": "Pérez",
                "role": "Desarrollador",
                "identification_number": "1234567890",
                "email": "juan@example.com",
                "password": "Password123!",
                "status": "inactivo"
            }
        }
