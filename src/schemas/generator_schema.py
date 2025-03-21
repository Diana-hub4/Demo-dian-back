# src/schemas/generator_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Modelo de solicitud para crear un generador
class GeneratorRequest(BaseModel):
    id_payment_transfer: str = Field(..., description="ID de la transferencia de pago asociada")
    electronic_invoice: str = Field(..., description="Factura electrónica (Sí/No)")
    cufe: str = Field(..., description="Código Único de Factura Electrónica (CUFE)")
    qr_code: str = Field(..., description="Código QR de la factura")
    invoice_pdf: Optional[bytes] = Field(None, description="PDF de la factura en formato binario")

# Modelo de respuesta para el generador
class GeneratorResponse(BaseModel):
    id: str = Field(..., description="ID único del generador")
    id_payment_transfer: str = Field(..., description="ID de la transferencia de pago asociada")
    electronic_invoice: str = Field(..., description="Factura electrónica (Sí/No)")
    cufe: str = Field(..., description="Código Único de Factura Electrónica (CUFE)")
    qr_code: str = Field(..., description="Código QR de la factura")
    invoice_pdf: Optional[bytes] = Field(None, description="PDF de la factura en formato binario")
    created_at: datetime = Field(..., description="Fecha de creación del generador")