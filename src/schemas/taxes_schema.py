# src/schemas/taxes_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

# Modelo de solicitud para crear un impuesto
class TaxRequest(BaseModel):
    id_invoice_receipt: str = Field(..., description="ID de la factura/recibo asociado al impuesto")
    tax_advance: str = Field(..., description="Anticipo de impuestos (Sí/No)")
    contributions: str = Field(..., description="Aportes (Sí/No)")
    withholding_tax_1: str = Field(..., description="Retención en la fuente 1 (Sí/No)")
    withholding_tax_varying: str = Field(..., description="Retención en la fuente variable (Sí/No)")
    commercial_debtors: str = Field(..., description="Deudores comerciales (Sí/No)")

# Modelo de respuesta para el impuesto
class TaxResponse(BaseModel):
    id: str = Field(..., description="ID único del impuesto")
    id_invoice_receipt: str = Field(..., description="ID de la factura/recibo asociado al impuesto")
    tax_advance: str = Field(..., description="Anticipo de impuestos (Sí/No)")
    contributions: str = Field(..., description="Aportes (Sí/No)")
    withholding_tax_1: str = Field(..., description="Retención en la fuente 1 (Sí/No)")
    withholding_tax_varying: str = Field(..., description="Retención en la fuente variable (Sí/No)")
    commercial_debtors: str = Field(..., description="Deudores comerciales (Sí/No)")
    created_at: datetime = Field(..., description="Fecha de creación del impuesto")