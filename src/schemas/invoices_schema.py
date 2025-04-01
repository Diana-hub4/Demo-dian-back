# src/schemas/invoicesReceipts_schema.py
from pydantic import BaseModel, Field
from datetime import datetime

# Modelo de solicitud para crear una factura/recibo
class InvoiceRequest(BaseModel):
    id_client: str = Field(..., description="ID del cliente asociado a la factura/recibo")
    electronic_invoice: str = Field(..., description="Factura electrónica (Sí/No)")
    electronic_payroll: str = Field(..., description="Nómina electrónica (Sí/No)")
    support_document: str = Field(..., description="Documento de soporte (Sí/No)")
    asset: str = Field(..., description="Activo (Sí/No)")
    liability: str = Field(..., description="Pasivo (Sí/No)")
    equity: str = Field(..., description="Patrimonio (Sí/No)")
    non_supported_expenses: str = Field(..., description="Gastos no soportados (Sí/No)")
    production_costs: str = Field(..., description="Costos de producción (Sí/No)")

# Modelo de respuesta para la factura/recibo
class InvoiceResponse(BaseModel):
    id: str = Field(..., description="ID único de la factura/recibo")
    id_client: str = Field(..., description="ID del cliente asociado a la factura/recibo")
    electronic_invoice: str = Field(..., description="Factura electrónica (Sí/No)")
    electronic_payroll: str = Field(..., description="Nómina electrónica (Sí/No)")
    support_document: str = Field(..., description="Documento de soporte (Sí/No)")
    asset: str = Field(..., description="Activo (Sí/No)")
    liability: str = Field(..., description="Pasivo (Sí/No)")
    equity: str = Field(..., description="Patrimonio (Sí/No)")
    non_supported_expenses: str = Field(..., description="Gastos no soportados (Sí/No)")
    production_costs: str = Field(..., description="Costos de producción (Sí/No)")
    created_at: datetime = Field(..., description="Fecha de creación de la factura/recibo")

class InvoicesJsonSchema(BaseModel):

    id: int
    plan_cliente: str  # 'gratuito', 'plus', 'pro', 'premium'
    facturas_usadas: int
    total_bruto: float
    descuentos: float
    subtotal: float
    retefuente: float
    reteica: float  
    copago_anticipo: float
    total_neto: float
    fecha_emision: datetime = datetime.now()
    estado: str = "pendiente"  # 'pendiente', 'enviada', 'cancelada'
    formas_pago: list = []  #'tarjeta credito', 'tarjeta debito', 'efectivo', 'transferencia bancaria'