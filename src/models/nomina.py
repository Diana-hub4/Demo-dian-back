import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Float
from .model import Model, Base
from marshmallow import Schema, fields

class Nomina(Model, Base):
    __tablename__ = 'nomina'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)  # Relación con el usuario (contador)
    contract_type = Column(Enum('obra_labor', 'prestacion_servicios', 'fijo', 'indefinido', 'aprendiz'), nullable=False)  # Tipo de contrato
    period = Column(String(7), nullable=False)  # Periodo (mes y año, formato YYYY-MM)
    employee_name = Column(String(255), nullable=False)  # Nombre del empleado
    salary = Column(Float, nullable=False)  # Salario bruto
    deductions = Column(Float, default=0.0)  # Deducciones (sanciones, descuentos, etc.)
    email = Column(String(255), nullable=False)  # Correo electrónico del empleado
    contributions = Column(Float, nullable=False)  # Aportes (salud, pensión, ARL, etc.)

    def __init__(self, id_user, contract_type, period, employee_name, salary, deductions, email, contributions):
        Model.__init__(self)
        self.id_user = id_user
        self.contract_type = contract_type
        self.period = period
        self.employee_name = employee_name
        self.salary = salary
        self.deductions = deductions
        self.email = email
        self.contributions = contributions

# Esquema para serializar/deserializar la tabla Nomina
class NominaJsonSchema(Schema):
    id = fields.Str()
    id_user = fields.Str()
    contract_type = fields.Str()
    period = fields.Str()
    employee_name = fields.Str()
    salary = fields.Float()
    deductions = fields.Float()
    email = fields.Str()
    contributions = fields.Float()

# Función para crear una nueva nómina
def create_nomina(id_user, contract_type, period, employee_name, salary, deductions, email, contributions):
    """
    Crea una nueva nómina en la tabla nomina.
    Retorna el objeto Nomina si el registro es exitoso.
    """
    # Verifica si ya existe una nómina para el mismo empleado en el mismo período
    existing_nomina = Nomina.query.filter((Nomina.employee_name == employee_name) & (Nomina.period == period)).first()
    if existing_nomina:
        raise ValueError("Ya existe una nómina para este empleado en el período especificado.")

    # Crea una nueva nómina
    new_nomina = Nomina(
        id_user=id_user,
        contract_type=contract_type,
        period=period,
        employee_name=employee_name,
        salary=salary,
        deductions=deductions,
        email=email,
        contributions=contributions
    )
    return new_nomina