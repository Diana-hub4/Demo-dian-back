# src/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import SessionSql, init_db, get_db
from src.models.login import User
from src.routes import user_routes  # Asumiendo que pusiste el endpoint en user_routes.py
from src.models import register, RegisterJsonSchema, register  # Cambia User por Register

app = FastAPI()

# Inicializar base de datos al inicio
@app.on_event("startup")
def startup():
    print("Creando base de datos...")
    init_db()
    print("Base de datos lista.")

# Dependency para obtener sesión de la DB
def get_db():
    db = SessionSql()
    try:
        yield db
    finally:
        db.close()

# Endpoint de prueba para insertar y obtener usuarios
app.include_router(user_routes.router)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(register).all()
    schema = RegisterJsonSchema(many=True)
    return schema.dump(users)
