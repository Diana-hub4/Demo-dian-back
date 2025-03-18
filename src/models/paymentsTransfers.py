import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class PaymentsTransfers(Model, Base):
    __tablename__ = 'payments_transfers'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_tax = Column(String(36), ForeignKey('taxes.id'), nullable=False)
    bank_transfer = Column(String(5))
    cash_payment = Column(String(5))
    credit_card_payment = Column(String(5))
    debit_card_payment = Column(String(5))
    barter = Column(String(5))

    def __init__(self, id_tax, bank_transfer, cash_payment, credit_card_payment, debit_card_payment, barter):
        Model.__init__(self)
        self.id_tax = id_tax
        self.bank_transfer = bank_transfer
        self.cash_payment = cash_payment
        self.credit_card_payment = credit_card_payment
        self.debit_card_payment = debit_card_payment
        self.barter = barter

class PaymentsTransfersJsonSchema(Schema):
    id = fields.Str()
    id_tax = fields.Str()
    bank_transfer = fields.Str()
    cash_payment = fields.Str()
    credit_card_payment = fields.Str()
    debit_card_payment = fields.Str()
    barter = fields.Str()
