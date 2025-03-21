# src/schemas/dianVerification_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

# Modelo de solicitud para crear una verificación DIAN
class DianVerificationRequest(BaseModel):
    id_generator: str = Field(..., description="ID del generador asociado a la verificación")
    requirements_check: str = Field(..., description="Verificación de requisitos (Sí/No)")
    copy_sent_to_client: str = Field(..., description="Copia enviada al cliente (Sí/No)")

# Modelo de respuesta para la verificación DIAN
class DianVerificationResponse(BaseModel):
    id: str = Field(..., description="ID único de la verificación DIAN")
    id_generator: str = Field(..., description="ID del generador asociado a la verificación")
    requirements_check: str = Field(..., description="Verificación de requisitos (Sí/No)")
    copy_sent_to_client: str = Field(..., description="Copia enviada al cliente (Sí/No)")
    created_at: datetime = Field(..., description="Fecha de creación de la verificación DIAN")