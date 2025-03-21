# src/routes/dianVerification_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.dianVerification import DianVerification
from ..schemas.dianVerification_schema import DianVerificationRequest, DianVerificationResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva verificación DIAN
@router.post("/dian-verifications", response_model=DianVerificationResponse)
async def create_dian_verification(verification: DianVerificationRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear una nueva verificación DIAN
        new_verification = DianVerification(
            id_generator=verification.id_generator,
            requirements_check=verification.requirements_check,
            copy_sent_to_client=verification.copy_sent_to_client
        )
        db.add(new_verification)
        db.commit()
        db.refresh(new_verification)
        return new_verification
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todas las verificaciones DIAN
@router.get("/dian-verifications", response_model=List[DianVerificationResponse])
async def get_all_dian_verifications(db: SessionLocal = Depends(get_db)):
    try:
        verifications = db.query(DianVerification).all()
        return verifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener una verificación DIAN por ID
@router.get("/dian-verifications/{verification_id}", response_model=DianVerificationResponse)
async def get_dian_verification_by_id(verification_id: str, db: SessionLocal = Depends(get_db)):
    try:
        verification = db.query(DianVerification).filter(DianVerification.id == verification_id).first()
        if not verification:
            raise HTTPException(status_code=404, detail="Verificación DIAN no encontrada")
        return verification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar una verificación DIAN
@router.put("/dian-verifications/{verification_id}", response_model=DianVerificationResponse)
async def update_dian_verification(verification_id: str, verification: DianVerificationRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_verification = db.query(DianVerification).filter(DianVerification.id == verification_id).first()
        if not existing_verification:
            raise HTTPException(status_code=404, detail="Verificación DIAN no encontrada")

        # Actualizar los campos de la verificación DIAN
        existing_verification.id_generator = verification.id_generator
        existing_verification.requirements_check = verification.requirements_check
        existing_verification.copy_sent_to_client = verification.copy_sent_to_client

        db.commit()
        db.refresh(existing_verification)
        return existing_verification
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar una verificación DIAN
@router.delete("/dian-verifications/{verification_id}")
async def delete_dian_verification(verification_id: str, db: SessionLocal = Depends(get_db)):
    try:
        verification = db.query(DianVerification).filter(DianVerification.id == verification_id).first()
        if not verification:
            raise HTTPException(status_code=404, detail="Verificación DIAN no encontrada")

        db.delete(verification)
        db.commit()
        return {"message": "Verificación DIAN eliminada correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))