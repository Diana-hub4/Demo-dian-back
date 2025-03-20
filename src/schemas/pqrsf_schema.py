# src/schemas/pqrsf_schema.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PQRSFRequest(BaseModel):
    pqrsf_type: str  # Tipo de PQRSF
    message: str     # Mensaje de la solicitud

class PQRSFResponse(BaseModel):
    id: str
    pqrsf_type: str
    message: str
    created_at: datetime