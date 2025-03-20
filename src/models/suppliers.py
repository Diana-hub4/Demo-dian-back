import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class Supplier(Model, Base):
    __tablename__ = 'suppliers'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)  # Relación con el usuario (contador)
    name = Column(String(255), nullable=False)  # Nombre del proveedor
    person_type = Column(Enum('Natural', 'Legal', 'Company'), nullable=False)  # Tipo de persona (Natural, Jurídica, Empresa)
    tax_id = Column(String(255), nullable=False)  # NIT o Cédula con dígito de verificación
    document_type = Column(Enum('id_card', 'foreign_id', 'other'), nullable=False)  # Tipo de documento (Cédula, Extranjería, Otro)
    identification_number = Column(String(255), nullable=False)  # Número de identificación
    business_reason = Column(String(255), nullable=False)  # Razón del negocio (parqueadero, comida, etc.)
    email = Column(String(255), nullable=False)  # Correo electrónico
    contact_number = Column(String(255), nullable=False)  # Número de contacto
    address = Column(String(255), nullable=False)  # Dirección
    city = Column(String(255), nullable=False)  # Ciudad
    regime_type = Column(Enum('Simplified', 'Common', 'Special'), nullable=False)  # Tipo de régimen (Simplificado, Común, Especial)
    status = Column(Enum('active', 'inactive'), default='active')  # Estado del proveedor (activo o inactivo)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Fecha de creación del proveedor

    def __init__(self, id_user, name, person_type, tax_id, document_type, identification_number, business_reason, email, contact_number, address, city, regime_type, status='active'):
        Model.__init__(self)
        self.id_user = id_user
        self.name = name
        self.person_type = person_type
        self.tax_id = tax_id
        self.document_type = document_type
        self.identification_number = identification_number
        self.business_reason = business_reason
        self.email = email
        self.contact_number = contact_number
        self.address = address
        self.city = city
        self.regime_type = regime_type
        self.status = status

# Esquema para serializar/deserializar la tabla Supplier
class SupplierJsonSchema(Schema):
    id = fields.Str()
    id_user = fields.Str()
    name = fields.Str()
    person_type = fields.Str()
    tax_id = fields.Str()
    document_type = fields.Str()
    identification_number = fields.Str()
    business_reason = fields.Str()
    email = fields.Str()
    contact_number = fields.Str()
    address = fields.Str()
    city = fields.Str()
    regime_type = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()

# Función para crear un nuevo proveedor
def create_supplier(id_user, name, person_type, tax_id, document_type, identification_number, business_reason, email, contact_number, address, city, regime_type, status='active'):
    """
    Crea un nuevo proveedor en la tabla suppliers.
    Retorna el objeto Supplier si el registro es exitoso.
    """
    # Verifica si el proveedor ya existe (por ejemplo, por NIT o correo electrónico)
    existing_supplier = Supplier.query.filter((Supplier.tax_id == tax_id) | (Supplier.email == email)).first()
    if existing_supplier:
        raise ValueError("El proveedor ya está registrado.")

    # Crea un nuevo proveedor
    new_supplier = Supplier(
        id_user=id_user,
        name=name,
        person_type=person_type,
        tax_id=tax_id,
        document_type=document_type,
        identification_number=identification_number,
        business_reason=business_reason,
        email=email,
        contact_number=contact_number,
        address=address,
        city=city,
        regime_type=regime_type,
        status=status
    )
    return new_supplier