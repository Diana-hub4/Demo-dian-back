# src/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import SessionSql, init_db, get_db
from src.models.register import Register, RegisterJsonSchema
from src.routes import register_routes  
from fastapi.middleware.cors import CORSMiddleware


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
app.include_router(register_routes.router)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    register = db.query(Register).all()
    schema = RegisterJsonSchema(many=True)
    return schema.dump(register)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Define el origen de las peticiones permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los headers
)