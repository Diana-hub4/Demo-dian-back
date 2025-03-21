# src/schemas/nomina_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Enums para validar los tipos de datos
class ContractType(str, Enum):
    OBRA_LABOR = "obra_labor"
    PRESTACION_SERVICIOS = "prestacion_servicios"
    FIJO = "fijo"
    INDEFINIDO = "indefinido"
    APRENDIZ = "aprendiz"

# Modelo de solicitud para crear una nómina
class NominaRequest(BaseModel):
    id_user: str = Field(..., description="ID del usuario (contador) asociado a la nómina")
    contract_type: ContractType = Field(..., description="Tipo de contrato (obra_labor, prestacion_servicios, fijo, indefinido, aprendiz)")
    period: str = Field(..., description="Periodo de la nómina (formato YYYY-MM)")
    employee_name: str = Field(..., description="Nombre del empleado")
    salary: float = Field(..., description="Salario bruto del empleado")
    deductions: float = Field(default=0.0, description="Deducciones (sanciones, descuentos, etc.)")
    email: str = Field(..., description="Correo electrónico del empleado")
    contributions: float = Field(..., description="Aportes (salud, pensión, ARL, etc.)")

# Modelo de respuesta para la nómina
class NominaResponse(BaseModel):
    id: str = Field(..., description="ID único de la nómina")
    id_user: str = Field(..., description="ID del usuario (contador) asociado a la nómina")
    contract_type: str = Field(..., description="Tipo de contrato (obra_labor, prestacion_servicios, fijo, indefinido, aprendiz)")
    period: str = Field(..., description="Periodo de la nómina (formato YYYY-MM)")
    employee_name: str = Field(..., description="Nombre del empleado")
    salary: float = Field(..., description="Salario bruto del empleado")
    deductions: float = Field(..., description="Deducciones (sanciones, descuentos, etc.)")
    email: str = Field(..., description="Correo electrónico del empleado")
    contributions: float = Field(..., description="Aportes (salud, pensión, ARL, etc.)")
    created_at: datetime = Field(..., description="Fecha de creación de la nómina")