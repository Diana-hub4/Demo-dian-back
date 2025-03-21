# src/schemas/paymentsTransfers_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

# Modelo de solicitud para crear un pago/transferencia
class PaymentsTransfersRequest(BaseModel):
    id_tax: str = Field(..., description="ID del impuesto asociado al pago/transferencia")
    bank_transfer: str = Field(..., description="Transferencia bancaria (Sí/No)")
    cash_payment: str = Field(..., description="Pago en efectivo (Sí/No)")
    credit_card_payment: str = Field(..., description="Pago con tarjeta de crédito (Sí/No)")
    debit_card_payment: str = Field(..., description="Pago con tarjeta débito (Sí/No)")
    barter: str = Field(..., description="Trueque (Sí/No)")

# Modelo de respuesta para el pago/transferencia
class PaymentsTransfersResponse(BaseModel):
    id: str = Field(..., description="ID único del pago/transferencia")
    id_tax: str = Field(..., description="ID del impuesto asociado al pago/transferencia")
    bank_transfer: str = Field(..., description="Transferencia bancaria (Sí/No)")
    cash_payment: str = Field(..., description="Pago en efectivo (Sí/No)")
    credit_card_payment: str = Field(..., description="Pago con tarjeta de crédito (Sí/No)")
    debit_card_payment: str = Field(..., description="Pago con tarjeta débito (Sí/No)")
    barter: str = Field(..., description="Trueque (Sí/No)")
    created_at: datetime = Field(..., description="Fecha de creación del pago/transferencia")