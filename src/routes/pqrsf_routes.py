# src/routes/pqrsf_routes.py
import uuid 
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from typing import List
from ..models.pqrsf import PQRSF
from ..schemas.pqrsf_schema import PQRSFRequest, PQRSFResponse
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from src.models.pqrsf import PQRSF  # Asegúrate que este modelo existe
import os
import shutil
from datetime import datetime
from typing import List

router = APIRouter(prefix="/pqrsf", tags=["PQRSF"])

UPLOAD_DIR = "uploads/pqrsf"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def crear_pqrsf(
    tipo: str = Form(...),
    mensaje: str = Form(...),
    archivos: List[UploadFile] = File([]),  # Lista de archivos (opcional)
    db: Session = Depends(get_db)
):
    try:
        nombres_archivos = []
        for archivo in archivos:
            if not archivo.filename.lower().endswith(('.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png')):
                continue  # O devuelve un error 400
            
            file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{archivo.filename}")
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(archivo.file, buffer)
            nombres_archivos.append(file_path)

        nueva_pqrsf = PQRSF(
            tipo=tipo,
            mensaje=mensaje,
            archivos=nombres_archivos,  # Asegúrate de que sea JSON-compatible
            fecha=datetime.utcnow(),
            estado="recibido"
        )
        db.add(nueva_pqrsf)
        db.commit()
        db.refresh(nueva_pqrsf)

        return {
            "status": "success",
            "message": "PQRSF registrada correctamente",
            "data": {
                "id": nueva_pqrsf.id,
                "tipo": nueva_pqrsf.tipo,
                "fecha": nueva_pqrsf.fecha
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar PQRSF: {str(e)}"
        )

    finally:
        db.close()