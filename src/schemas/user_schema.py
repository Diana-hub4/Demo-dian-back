# src/schemas/user_schema.py

from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    last_name: str
    role: str
    identification_number: str
    email: str
    permissions: str | None = None
