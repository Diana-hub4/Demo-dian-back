# src/routes/generator_routes.py
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from ..models.generator import Generator
from ..schemas.generator_schema import GeneratorRequest, GeneratorResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo generador
@router.post("/generators", response_model=GeneratorResponse)
async def create_generator(
    id_payment_transfer: str,
    electronic_invoice: str,
    cufe: str,
    qr_code: str,
    invoice_pdf: Optional[UploadFile] = File(None),
    db: SessionLocal = Depends(get_db)
):
    try:
        # Leer el archivo PDF si se proporciona
        pdf_content = None
        if invoice_pdf:
            pdf_content = await invoice_pdf.read()

        # Crear un nuevo generador
        new_generator = Generator(
            id_payment_transfer=id_payment_transfer,
            electronic_invoice=electronic_invoice,
            cufe=cufe,
            qr_code=qr_code,
            invoice_pdf=pdf_content
        )
        db.add(new_generator)
        db.commit()
        db.refresh(new_generator)
        return new_generator
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los generadores
@router.get("/generators", response_model=List[GeneratorResponse])
async def get_all_generators(db: SessionLocal = Depends(get_db)):
    try:
        generators = db.query(Generator).all()
        return generators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un generador por ID
@router.get("/generators/{generator_id}", response_model=GeneratorResponse)
async def get_generator_by_id(generator_id: str, db: SessionLocal = Depends(get_db)):
    try:
        generator = db.query(Generator).filter(Generator.id == generator_id).first()
        if not generator:
            raise HTTPException(status_code=404, detail="Generador no encontrado")
        return generator
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un generador
@router.put("/generators/{generator_id}", response_model=GeneratorResponse)
async def update_generator(
    generator_id: str,
    id_payment_transfer: str,
    electronic_invoice: str,
    cufe: str,
    qr_code: str,
    invoice_pdf: Optional[UploadFile] = File(None),
    db: SessionLocal = Depends(get_db)
):
    try:
        existing_generator = db.query(Generator).filter(Generator.id == generator_id).first()
        if not existing_generator:
            raise HTTPException(status_code=404, detail="Generador no encontrado")

        # Leer el archivo PDF si se proporciona
        pdf_content = None
        if invoice_pdf:
            pdf_content = await invoice_pdf.read()

        # Actualizar los campos del generador
        existing_generator.id_payment_transfer = id_payment_transfer
        existing_generator.electronic_invoice = electronic_invoice
        existing_generator.cufe = cufe
        existing_generator.qr_code = qr_code
        if pdf_content:
            existing_generator.invoice_pdf = pdf_content

        db.commit()
        db.refresh(existing_generator)
        return existing_generator
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un generador
@router.delete("/generators/{generator_id}")
async def delete_generator(generator_id: str, db: SessionLocal = Depends(get_db)):
    try:
        generator = db.query(Generator).filter(Generator.id == generator_id).first()
        if not generator:
            raise HTTPException(status_code=404, detail="Generador no encontrado")

        db.delete(generator)
        db.commit()
        return {"message": "Generador eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))