# src/schemas/clients_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# Enums para validar los tipos de datos
class PersonType(str, Enum):
    NATURAL = "Natural"
    LEGAL = "Legal"
    COMPANY = "Company"

class DocumentType(str, Enum):
    ID_CARD = "id_card"
    FOREIGN_ID = "foreign_id"
    OTHER = "other"

class RegimeType(str, Enum):
    SIMPLIFIED = "Simplified"
    COMMON = "Common"
    SPECIAL = "Special"

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Modelo de solicitud para crear un cliente
class ClientRequest(BaseModel):
    id_user: str = Field(..., description="ID del usuario (contador) asociado al cliente")
    name: str = Field(..., description="Nombre del cliente")
    person_type: PersonType = Field(..., description="Tipo de persona (Natural, Jurídica, Empresa)")
    tax_id: str = Field(..., description="NIT o Cédula con dígito de verificación")
    document_type: DocumentType = Field(..., description="Tipo de documento (Cédula, Extranjería, Otro)")
    identification_number: str = Field(..., description="Número de identificación")
    business_reason: str = Field(..., description="Razón del negocio (parqueadero, comida, etc.)")
    email: str = Field(..., description="Correo electrónico")
    contact_number: str = Field(..., description="Número de contacto")
    address: str = Field(..., description="Dirección")
    city: str = Field(..., description="Ciudad")
    regime_type: RegimeType = Field(..., description="Tipo de régimen (Simplificado, Común, Especial)")
    status: Optional[Status] = Field(default=Status.ACTIVE, description="Estado del cliente (activo o inactivo)")

# Modelo de respuesta para el cliente
class ClientResponse(BaseModel):
    id: str = Field(..., description="ID único del cliente")
    id_user: str = Field(..., description="ID del usuario (contador) asociado al cliente")
    name: str = Field(..., description="Nombre del cliente")
    person_type: str = Field(..., description="Tipo de persona (Natural, Jurídica, Empresa)")
    tax_id: str = Field(..., description="NIT o Cédula con dígito de verificación")
    document_type: str = Field(..., description="Tipo de documento (Cédula, Extranjería, Otro)")
    identification_number: str = Field(..., description="Número de identificación")
    business_reason: str = Field(..., description="Razón del negocio (parqueadero, comida, etc.)")
    email: str = Field(..., description="Correo electrónico")
    contact_number: str = Field(..., description="Número de contacto")
    address: str = Field(..., description="Dirección")
    city: str = Field(..., description="Ciudad")
    regime_type: str = Field(..., description="Tipo de régimen (Simplificado, Común, Especial)")
    status: str = Field(..., description="Estado del cliente (activo o inactivo)")
    created_at: datetime = Field(..., description="Fecha de creación del cliente")

class ClientCreateSchema(BaseModel):
    id_user: str
    name: str
    person_type: str
    tax_id: str
    document_type: str
    identification_number: str
    business_reason: str
    email: str
    contact_number: str
    address: str
    city: str
    regime_type: str
    status: Optional[str] = 'active'