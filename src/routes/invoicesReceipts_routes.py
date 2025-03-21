# src/routes/invoicesReceipts_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.invoicesReceipts import InvoicesReceipts
from ..schemas.invoicesReceipts_schema import InvoicesReceiptsRequest, InvoicesReceiptsResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva factura/recibo
@router.post("/invoices-receipts", response_model=InvoicesReceiptsResponse)
async def create_invoice_receipt(invoice: InvoicesReceiptsRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear una nueva factura/recibo
        new_invoice = InvoicesReceipts(
            id_client=invoice.id_client,
            electronic_invoice=invoice.electronic_invoice,
            electronic_payroll=invoice.electronic_payroll,
            support_document=invoice.support_document,
            asset=invoice.asset,
            liability=invoice.liability,
            equity=invoice.equity,
            non_supported_expenses=invoice.non_supported_expenses,
            production_costs=invoice.production_costs
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)
        return new_invoice
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todas las facturas/recibos
@router.get("/invoices-receipts", response_model=List[InvoicesReceiptsResponse])
async def get_all_invoices_receipts(db: SessionLocal = Depends(get_db)):
    try:
        invoices_receipts = db.query(InvoicesReceipts).all()
        return invoices_receipts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener una factura/recibo por ID
@router.get("/invoices-receipts/{invoice_id}", response_model=InvoicesReceiptsResponse)
async def get_invoice_receipt_by_id(invoice_id: str, db: SessionLocal = Depends(get_db)):
    try:
        invoice_receipt = db.query(InvoicesReceipts).filter(InvoicesReceipts.id == invoice_id).first()
        if not invoice_receipt:
            raise HTTPException(status_code=404, detail="Factura/Recibo no encontrado")
        return invoice_receipt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar una factura/recibo
@router.put("/invoices-receipts/{invoice_id}", response_model=InvoicesReceiptsResponse)
async def update_invoice_receipt(invoice_id: str, invoice: InvoicesReceiptsRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_invoice = db.query(InvoicesReceipts).filter(InvoicesReceipts.id == invoice_id).first()
        if not existing_invoice:
            raise HTTPException(status_code=404, detail="Factura/Recibo no encontrado")

        # Actualizar los campos de la factura/recibo
        existing_invoice.id_client = invoice.id_client
        existing_invoice.electronic_invoice = invoice.electronic_invoice
        existing_invoice.electronic_payroll = invoice.electronic_payroll
        existing_invoice.support_document = invoice.support_document
        existing_invoice.asset = invoice.asset
        existing_invoice.liability = invoice.liability
        existing_invoice.equity = invoice.equity
        existing_invoice.non_supported_expenses = invoice.non_supported_expenses
        existing_invoice.production_costs = invoice.production_costs

        db.commit()
        db.refresh(existing_invoice)
        return existing_invoice
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar una factura/recibo
@router.delete("/invoices-receipts/{invoice_id}")
async def delete_invoice_receipt(invoice_id: str, db: SessionLocal = Depends(get_db)):
    try:
        invoice_receipt = db.query(InvoicesReceipts).filter(InvoicesReceipts.id == invoice_id).first()
        if not invoice_receipt:
            raise HTTPException(status_code=404, detail="Factura/Recibo no encontrado")

        db.delete(invoice_receipt)
        db.commit()
        return {"message": "Factura/Recibo eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))