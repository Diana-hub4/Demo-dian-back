from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.register import User
from src.schemas.register_schema import UserJsonSchema

router = APIRouter()

@router.post("/users/")
def create_user(register: UserJsonSchema, db: Session = Depends(get_db)):
    print("📩 Body recibido:", register.dict())  
    # Verificar si el correo electrónico ya está registrado
    existing_user_email = db.query(User).filter(User.email == register.email).first()
    existing_user_id = db.query(User).filter(
        User.identification_number == register.identification_number
    ).first()
    if existing_user_email or existing_user_id:
        raise HTTPException(status_code=400, detail="El Usuario ya se encuentra registrado.")

    # Crear un nuevo usuario
    db_user = User(
        first_name=register.first_name,
        last_name=register.last_name,
        role=register.role,  # Ahora el rol se recibe desde el esquema
        identification_number=register.identification_number,
        email=register.email,
        permissions=register.permissions,  # Ahora los permisos se reciben desde el esquema
        password=register.password,  # La contraseña se encriptará automáticamente en el modelo
        status=register.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Usuario creado", "user": db_user}

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user