# src/routes/taxes_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.taxes import Tax
from ..schemas.taxes_schema import TaxRequest, TaxResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo impuesto
@router.post("/taxes", response_model=TaxResponse)
async def create_tax(tax: TaxRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear un nuevo impuesto
        new_tax = Tax(
            id_invoice_receipt=tax.id_invoice_receipt,
            tax_advance=tax.tax_advance,
            contributions=tax.contributions,
            withholding_tax_1=tax.withholding_tax_1,
            withholding_tax_varying=tax.withholding_tax_varying,
            commercial_debtors=tax.commercial_debtors
        )
        db.add(new_tax)
        db.commit()
        db.refresh(new_tax)
        return new_tax
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los impuestos
@router.get("/taxes", response_model=List[TaxResponse])
async def get_all_taxes(db: SessionLocal = Depends(get_db)):
    try:
        taxes = db.query(Tax).all()
        return taxes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un impuesto por ID
@router.get("/taxes/{tax_id}", response_model=TaxResponse)
async def get_tax_by_id(tax_id: str, db: SessionLocal = Depends(get_db)):
    try:
        tax = db.query(Tax).filter(Tax.id == tax_id).first()
        if not tax:
            raise HTTPException(status_code=404, detail="Impuesto no encontrado")
        return tax
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un impuesto
@router.put("/taxes/{tax_id}", response_model=TaxResponse)
async def update_tax(tax_id: str, tax: TaxRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_tax = db.query(Tax).filter(Tax.id == tax_id).first()
        if not existing_tax:
            raise HTTPException(status_code=404, detail="Impuesto no encontrado")

        # Actualizar los campos del impuesto
        existing_tax.id_invoice_receipt = tax.id_invoice_receipt
        existing_tax.tax_advance = tax.tax_advance
        existing_tax.contributions = tax.contributions
        existing_tax.withholding_tax_1 = tax.withholding_tax_1
        existing_tax.withholding_tax_varying = tax.withholding_tax_varying
        existing_tax.commercial_debtors = tax.commercial_debtors

        db.commit()
        db.refresh(existing_tax)
        return existing_tax
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un impuesto
@router.delete("/taxes/{tax_id}")
async def delete_tax(tax_id: str, db: SessionLocal = Depends(get_db)):
    try:
        tax = db.query(Tax).filter(Tax.id == tax_id).first()
        if not tax:
            raise HTTPException(status_code=404, detail="Impuesto no encontrado")

        db.delete(tax)
        db.commit()
        return {"message": "Impuesto eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))