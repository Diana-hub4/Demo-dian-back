# src/routes/suppliers_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.suppliers import Supplier, create_supplier
from ..schemas.suppliers_schema import SupplierRequest, SupplierResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo proveedor
@router.post("/suppliers", response_model=SupplierResponse)
async def create_new_supplier(supplier: SupplierRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear un nuevo proveedor
        new_supplier = create_supplier(
            id_user=supplier.id_user,
            name=supplier.name,
            person_type=supplier.person_type.value,
            tax_id=supplier.tax_id,
            document_type=supplier.document_type.value,
            identification_number=supplier.identification_number,
            business_reason=supplier.business_reason,
            email=supplier.email,
            contact_number=supplier.contact_number,
            address=supplier.address,
            city=supplier.city,
            regime_type=supplier.regime_type.value,
            status=supplier.status.value
        )
        db.add(new_supplier)
        db.commit()
        db.refresh(new_supplier)
        return new_supplier
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los proveedores
@router.get("/suppliers", response_model=List[SupplierResponse])
async def get_all_suppliers(db: SessionLocal = Depends(get_db)):
    try:
        suppliers = db.query(Supplier).all()
        return suppliers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un proveedor por ID
@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_by_id(supplier_id: str, db: SessionLocal = Depends(get_db)):
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return supplier
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un proveedor
@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(supplier_id: str, supplier: SupplierRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not existing_supplier:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

        # Actualizar los campos del proveedor
        existing_supplier.id_user = supplier.id_user
        existing_supplier.name = supplier.name
        existing_supplier.person_type = supplier.person_type.value
        existing_supplier.tax_id = supplier.tax_id
        existing_supplier.document_type = supplier.document_type.value
        existing_supplier.identification_number = supplier.identification_number
        existing_supplier.business_reason = supplier.business_reason
        existing_supplier.email = supplier.email
        existing_supplier.contact_number = supplier.contact_number
        existing_supplier.address = supplier.address
        existing_supplier.city = supplier.city
        existing_supplier.regime_type = supplier.regime_type.value
        existing_supplier.status = supplier.status.value

        db.commit()
        db.refresh(existing_supplier)
        return existing_supplier
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un proveedor
@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: str, db: SessionLocal = Depends(get_db)):
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

        db.delete(supplier)
        db.commit()
        return {"message": "Proveedor eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))