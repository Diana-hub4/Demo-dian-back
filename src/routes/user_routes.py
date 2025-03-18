# src/routes/user_routes.py


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User
from src.schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        last_name=user.last_name,
        role="client",  # Valor fijo
        identification_number=user.identification_number,
        email=user.email,
        permissions="client"  # Valor fijo
    )
    db.add(db_user)
    db.commit()
    return {"message": "Usuario creado"}
