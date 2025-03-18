import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class InvoicesReceipts(Model, Base):
    __tablename__ = 'invoices_receipts'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_client = Column(String(36), ForeignKey('clients.id'), nullable=False)
    electronic_invoice = Column(String(5))
    electronic_payroll = Column(String(5))
    support_document = Column(String(5))
    asset = Column(String(5))
    liability = Column(String(5))
    equity = Column(String(5))
    non_supported_expenses = Column(String(5))
    production_costs = Column(String(5))

    def __init__(self, id_client, electronic_invoice, electronic_payroll, support_document, asset, liability, equity, non_supported_expenses, production_costs):
        Model.__init__(self)
        self.id_client = id_client
        self.electronic_invoice = electronic_invoice
        self.electronic_payroll = electronic_payroll
        self.support_document = support_document
        self.asset = asset
        self.liability = liability
        self.equity = equity
        self.non_supported_expenses = non_supported_expenses
        self.production_costs = production_costs

class InvoicesReceiptsJsonSchema(Schema):
    id = fields.Str()
    id_client = fields.Str()
    electronic_invoice = fields.Str()
    electronic_payroll = fields.Str()
    support_document = fields.Str()
    asset = fields.Str()
    liability = fields.Str()
    equity = fields.Str()
    non_supported_expenses = fields.Str()
    production_costs = fields.Str()
