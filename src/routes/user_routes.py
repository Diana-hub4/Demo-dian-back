from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.register import Register, RegisterJsonSchema

router = APIRouter()

@router.post("/users/")
def create_user(user: RegisterJsonSchema, db: Session = Depends(get_db)):
    # Verificar si el correo electrónico ya está registrado
    existing_user = db.query(Register).filter(Register.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    # Crear un nuevo usuario
    db_user = Register(
        name=user.name,
        last_name=user.last_name,
        role=user.role,  # Ahora el rol se recibe desde el esquema
        identification_number=user.identification_number,
        email=user.email,
        permissions=user.permissions,  # Ahora los permisos se reciben desde el esquema
        password=user.password  # La contraseña se encriptará automáticamente en el modelo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario creado", "user": db_user}

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Register).filter(Register.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user