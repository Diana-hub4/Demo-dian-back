# src/routes/clients_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.clients import Client, create_client
from ..schemas.clients_schema import ClientRequest, ClientResponse
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo cliente
@router.post("/clients", response_model=ClientResponse)
async def create_new_client(client: ClientRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear un nuevo cliente
        new_client = create_client(
            id_user=client.id_user,
            name=client.name,
            person_type=client.person_type.value,
            tax_id=client.tax_id,
            document_type=client.document_type.value,
            identification_number=client.identification_number,
            business_reason=client.business_reason,
            email=client.email,
            contact_number=client.contact_number,
            address=client.address,
            city=client.city,
            regime_type=client.regime_type.value,
            status=client.status.value if client.status else "active"
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los clientes
@router.get("/clients", response_model=List[ClientResponse])
async def get_all_clients(db: SessionLocal = Depends(get_db)):
    try:
        clients = db.query(Client).all()
        return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un cliente por ID
@router.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client_by_id(client_id: str, db: SessionLocal = Depends(get_db)):
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para actualizar un cliente
@router.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(client_id: str, client: ClientRequest, db: SessionLocal = Depends(get_db)):
    try:
        existing_client = db.query(Client).filter(Client.id == client_id).first()
        if not existing_client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Actualizar los campos del cliente
        existing_client.id_user = client.id_user
        existing_client.name = client.name
        existing_client.person_type = client.person_type.value
        existing_client.tax_id = client.tax_id
        existing_client.document_type = client.document_type.value
        existing_client.identification_number = client.identification_number
        existing_client.business_reason = client.business_reason
        existing_client.email = client.email
        existing_client.contact_number = client.contact_number
        existing_client.address = client.address
        existing_client.city = client.city
        existing_client.regime_type = client.regime_type.value
        existing_client.status = client.status.value if client.status else "active"

        db.commit()
        db.refresh(existing_client)
        return existing_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para eliminar un cliente
@router.delete("/clients/{client_id}")
async def delete_client(client_id: str, db: SessionLocal = Depends(get_db)):
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db.delete(client)
        db.commit()
        return {"message": "Cliente eliminado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))