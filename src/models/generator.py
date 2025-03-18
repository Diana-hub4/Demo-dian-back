import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, LargeBinary
from .model import Model, Base
from marshmallow import Schema, fields

class Generator(Model, Base):
    __tablename__ = 'generator'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_payment_transfer = Column(String(36), ForeignKey('payments_transfers.id'), nullable=False)
    electronic_invoice = Column(String(5))
    cufe = Column(String(255))
    qr_code = Column(String(255))
    invoice_pdf = Column(LargeBinary)

    def __init__(self, id_payment_transfer, electronic_invoice, cufe, qr_code, invoice_pdf):
        Model.__init__(self)
        self.id_payment_transfer = id_payment_transfer
        self.electronic_invoice = electronic_invoice
        self.cufe = cufe
        self.qr_code = qr_code
        self.invoice_pdf = invoice_pdf

class GeneratorJsonSchema(Schema):
    id = fields.Str()
    id_payment_transfer = fields.Str()
    electronic_invoice = fields.Str()
    cufe = fields.Str()
    qr_code = fields.Str()
    invoice_pdf = fields.Raw()