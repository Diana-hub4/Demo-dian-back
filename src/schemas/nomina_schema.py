# src/schemas/nomina_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

# Enums para validar los tipos de datos
class ContractType(str, Enum):
    OBRA_LABOR = "obra_labor"
    PRESTACION_SERVICIOS = "prestacion_servicios"
    FIJO = "fijo"
    INDEFINIDO = "indefinido"
    APRENDIZ = "aprendiz"
class NominaCreate(BaseModel):
    id_user: str
    contract_type: ContractType
    period: str = Field(..., regex=r'^\d{4}-\d{2}$')
    employee_id: str
    employee_name: str
    base_salary: float
    transport_allowance: float = 0.0
    days_worked: float
    night_hours: float = 0.0
    extra_day_hours: float = 0.0
    extra_night_hours: float = 0.0
    sunday_hours: float = 0.0
    holiday_hours: float = 0.0
    deductions: float = 0.0
    other_concepts: Optional[List[str]] = None

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
class NominaResponse(NominaCreate):
    id: str
    health_contribution: float
    pension_contribution: float
    solidarity_pension_fund: float
    total_gross: float
    total_net: float
    is_paid: bool
    payment_date: Optional[date]
    pdf_url: Optional[str]
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id_user": "uuid-del-usuario",
                "employee_id": "123456789",
                "employee_name": "Juan Pérez",
                "contract_type": "indefinido",
                "period": "2023-10",
                "salario_base": 2500000,
                # ... etc ...
            }
        }