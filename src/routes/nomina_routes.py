# src/routes/nomina_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.nomina import Nomina, create_nomina
from ..schemas.nomina_schema import NominaRequest, NominaResponse
from ..database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva nómina
@router.post("/nomina", response_model=NominaResponse)
async def create_new_nomina(nomina: NominaRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear una nueva nómina
        new_nomina = create_nomina(
            id_user=nomina.id_user,
            contract_type=nomina.contract_type.value,
            period=nomina.period,
            employee_name=nomina.employee_name,
            salary=nomina.salary,
            deductions=nomina.deductions,
            email=nomina.email,
            contributions=nomina.contributions
        )
        db.add(new_nomina)
        db.commit()
        db.refresh(new_nomina)
        return new_nomina
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todas las nóminas
@router.get("/nomina", response_model=List[NominaResponse])
async def get_all_nominas(db: SessionLocal = Depends(get_db)):
    try:
        nominas = db.query(Nomina).all()
        return nominas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener una nómina por ID
@router.get("/nomina/{nomina_id}", response_model=NominaResponse)
async def get_nomina_by_id(nomina_id: str, db: SessionLocal = Depends(get_db)):
    try:
        nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
        if not nomina:
            raise HTTPException(status_code=404, detail="Nómina no encontrada")
        return nomina
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar una nómina
@router.put("/nomina/{nomina_id}", response_model=NominaResponse)
async def update_nomina(nomina_id: str, nomina: NominaRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
        if not existing_nomina:
            raise HTTPException(status_code=404, detail="Nómina no encontrada")

        # Actualizar los campos de la nómina
        existing_nomina.id_user = nomina.id_user
        existing_nomina.contract_type = nomina.contract_type.value
        existing_nomina.period = nomina.period
        existing_nomina.employee_name = nomina.employee_name
        existing_nomina.salary = nomina.salary
        existing_nomina.deductions = nomina.deductions
        existing_nomina.email = nomina.email
        existing_nomina.contributions = nomina.contributions

        db.commit()
        db.refresh(existing_nomina)
        return existing_nomina
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar una nómina
@router.delete("/nomina/{nomina_id}")
async def delete_nomina(nomina_id: str, db: SessionLocal = Depends(get_db)):
    try:
        nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
        if not nomina:
            raise HTTPException(status_code=404, detail="Nómina no encontrada")

        db.delete(nomina)
        db.commit()
        return {"message": "Nómina eliminada correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))