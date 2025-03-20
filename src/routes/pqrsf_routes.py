# src/routes/pqrsf_routes.py
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List
from ..models.pqrsf import PQRSF
from ..schemas.pqrsf_schema import PQRSFRequest, PQRSFResponse
from ..database import SessionLocal

router = APIRouter()

@router.post("/pqrsf", response_model=PQRSFResponse)
async def submit_pqrsf(
    pqrsf_type: str = Form(...),
    message: str = Form(...),
    files: List[UploadFile] = File(None)
):
    db = SessionLocal()
    try:
        # Crear una nueva PQRSF
        new_pqrsf = PQRSF(pqrsf_type=pqrsf_type, message=message)
        db.add(new_pqrsf)
        db.commit()
        db.refresh(new_pqrsf)

        # Procesar archivos adjuntos (si los hay)
        if files:
            for file in files:
                file_content = await file.read()
                # Aquí puedes guardar el archivo en el servidor o procesarlo
                print(f"Archivo recibido: {file.filename}")

        return new_pqrsf

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()