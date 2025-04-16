## src\models\nomina.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Float, Numeric, Boolean, JSON
from .model import Model, Base
from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as PyEnum
class TipoContrato(PyEnum):
    OBRA_LABOR = "obra_labor"
    PRESTACION_SERVICIOS = "prestacion_servicios"
    FIJO = "fijo"
    INDEFINIDO = "indefinido"
    APRENDIZ = "aprendiz"

class Nomina(Model, Base):
    __tablename__ = 'nomina'
    
    # Identificación y relación
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('users.id'), nullable=False)
    
    #Información del empleado
    employee_id = Column(String(20), nullable=False)  # Cédula del empleado
    employee_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    cargo = Column(String)  # Nuevo campo: cargo del empleado

    # Información del contrato y periodo
    contract_type = Column(Enum(TipoContrato), nullable=False)
    period = Column(String(7), nullable=False)  # YYYY-MM
    
    # Salarios e ingresos
    salario_base = Column(Numeric(12, 2), nullable=False)  # base_salary renombrado
    horas_extras = Column(Numeric(12, 2), default=0.0)  # Nuevo campo
    transporte = Column(Numeric(12, 2), default=0.0)  # transport_allowance renombrado
    vacaciones = Column(Numeric(12, 2), default=0.0)  # Nuevo campo
    total_ingresos = Column(Numeric(12, 2), default=0.0)  # Nuevo campo
    
    # Tiempo trabajado
    days_worked = Column(Numeric(5, 2), nullable=False)
    night_hours = Column(Numeric(5, 2), default=0.0)
    extra_day_hours = Column(Numeric(5, 2), default=0.0)
    extra_night_hours = Column(Numeric(5, 2), default=0.0)
    sunday_hours = Column(Numeric(5, 2), default=0.0)
    holiday_hours = Column(Numeric(5, 2), default=0.0)
    retrasos = Column(Numeric(12, 2), default=0.0) 
    
    # Deducciones y aportes
    health_contribution = Column(Numeric(12, 2), nullable=False)
    pension_contribution = Column(Numeric(12, 2), nullable=False)
    solidarity_pension_fund = Column(Numeric(12, 2), default=0.0)
    deductions = Column(Numeric(12, 2), default=0.0)
    total_deducciones = Column(Numeric(12, 2), default=0.0) 
    
    # Otros campos
    other_concepts = Column(JSON)  # Conceptos adicionales
    total_neto = Column(Numeric(12, 2), nullable=False)  # total_net renombrado
    is_paid = Column(Boolean, default=False)
    payment_date = Column(DateTime, nullable=True)
    pdf_url = Column(String, nullable=True)

def create_nomina(id_user, contract_type, period, employee_name, employee_id, email, 
                 salario_base, days_worked, health_contribution, pension_contribution,
                 **kwargs):
    """
    Crea una nueva nómina en la tabla nomina.
    Retorna el objeto Nomina si el registro es exitoso.
    
    Args:
        id_user: ID del usuario que crea la nómina
        contract_type: Tipo de contrato (enum TipoContrato)
        period: Periodo en formato YYYY-MM
        employee_name: Nombre del empleado
        employee_id: Identificación del empleado
        email: Email del empleado
        salario_base: Salario base del empleado
        days_worked: Días trabajados en el periodo
        health_contribution: Aporte a salud
        pension_contribution: Aporte a pensión
        **kwargs: Otros campos opcionales de la nómina
        
    Returns:
        Objeto Nomina creado
        
    Raises:
        ValueError: Si ya existe una nómina para este empleado en el período
    """
    # Verifica si ya existe una nómina para el mismo empleado en el mismo período
    existing_nomina = Nomina.query.filter(
        (Nomina.employee_id == employee_id) & 
        (Nomina.period == period)
    ).first()
    
    if existing_nomina:
        raise ValueError("Ya existe una nómina para este empleado en el período especificado.")

    # Crea una nueva nómina
    new_nomina = Nomina(
        id_user=id_user,
        contract_type=contract_type,
        period=period,
        employee_name=employee_name,
        employee_id=employee_id,
        email=email,
        salario_base=salario_base,
        days_worked=days_worked,
        health_contribution=health_contribution,
        pension_contribution=pension_contribution,
        **kwargs
    )
    
    return new_nomina