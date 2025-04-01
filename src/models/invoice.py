# models/invoice.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Numeric, Integer, Text
from .model import Model, Base
from marshmallow import Schema, fields, validate

class Invoice(Model, Base):
    __tablename__ = 'invoices'
    
    # Identificación
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_client = Column(String(36), ForeignKey('clients.id'), nullable=False)
    invoice_number = Column(String(50), unique=True, nullable=False)
    invoice_type = Column(String(20), nullable=False)  # Factura electrónica, nómina, etc.
    cufe = Column(String(100), unique=True)  # Código Único de Factura Electrónica
    qr_code = Column(Text)  # Datos del QR
    
    # Fechas
    issue_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    payment_due_date = Column(DateTime)
    
    # Cliente
    client_name = Column(String(100), nullable=False)
    client_id = Column(String(50), nullable=False)  # NIT/Cédula
    client_email = Column(String(100))
    
    # Totales
    subtotal = Column(Numeric(12, 2), nullable=False)
    total_discount = Column(Numeric(12, 2), default=0)
    total_taxes = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), nullable=False)
    
    # Retenciones
    tax_withholding = Column(Numeric(12, 2), default=0)  # Retefuente
    ica_withholding = Column(Numeric(12, 2), default=0)  # ReteICA
    
    # Estado
    status = Column(String(20), default='draft')  # draft, sent, paid, cancelled
    
    # Documentos adjuntos
    attached_documents = Column(Text)  # JSON con rutas de documentos
    
    # Métodos de pago
    payment_methods = Column(Text)  # JSON con métodos de pago
    
    def __init__(self, **kwargs):
        Model.__init__(self)
        for key, value in kwargs.items():
            setattr(self, key, value)

class InvoiceItem(Model, Base):
    __tablename__ = 'invoice_items'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey('invoices.id'), nullable=False)
    product_code = Column(String(50))
    product_name = Column(String(100), nullable=False)
    description = Column(Text)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    discount = Column(Numeric(5, 2), default=0)  # Porcentaje
    tax = Column(Numeric(5, 2), default=0)       # Porcentaje
    total = Column(Numeric(12, 2), nullable=False)

class InvoiceSchema(Schema):
    id = fields.Str()
    id_client = fields.Str(required=True)
    invoice_number = fields.Str(required=True)
    invoice_type = fields.Str(required=True)
    cufe = fields.Str()
    qr_code = fields.Str()
    issue_date = fields.DateTime()
    payment_due_date = fields.DateTime()
    client_name = fields.Str(required=True)
    client_id = fields.Str(required=True)
    client_email = fields.Str()
    subtotal = fields.Decimal(required=True)
    total_discount = fields.Decimal()
    total_taxes = fields.Decimal()
    total = fields.Decimal(required=True)
    tax_withholding = fields.Decimal()
    ica_withholding = fields.Decimal()
    status = fields.Str()
    attached_documents = fields.Str()
    payment_methods = fields.Str()

class InvoiceItemSchema(Schema):
    id = fields.Str()
    invoice_id = fields.Str(required=True)
    product_code = fields.Str()
    product_name = fields.Str(required=True)
    description = fields.Str()
    quantity = fields.Decimal(required=True)
    unit_price = fields.Decimal(required=True)
    discount = fields.Decimal()
    tax = fields.Decimal()
    total = fields.Decimal(required=True)