import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class Tax(Model, Base):
    __tablename__ = 'taxes'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_invoice_receipt = Column(String(36), ForeignKey('invoices_receipts.id'), nullable=False)
    tax_advance = Column(String(10))
    contributions = Column(String(10))
    withholding_tax_1 = Column(String(10))
    withholding_tax_varying = Column(String(10))
    commercial_debtors = Column(String(10))

    def __init__(self, id_invoice_receipt, tax_advance, contributions, withholding_tax_1, withholding_tax_varying, commercial_debtors):
        Model.__init__(self)
        self.id_invoice_receipt = id_invoice_receipt
        self.tax_advance = tax_advance
        self.contributions = contributions
        self.withholding_tax_1 = withholding_tax_1
        self.withholding_tax_varying = withholding_tax_varying
        self.commercial_debtors = commercial_debtors

class TaxJsonSchema(Schema):
    id = fields.Str()
    id_invoice_receipt = fields.Str()
    tax_advance = fields.Str()
    contributions = fields.Str()
    withholding_tax_1 = fields.Str()
    withholding_tax_varying = fields.Str()
    commercial_debtors = fields.Str()