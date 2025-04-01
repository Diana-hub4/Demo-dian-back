# src/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import SessionSql, init_db, get_db
from src.models.register import User, UserJsonSchema
from src.routes import login_routes, forgot_password_routes, register_routes  
from fastapi.middleware.cors import CORSMiddleware
from .business_logic.forgot_password_logic import request_password_reset
from .schemas.forgot_password_schemas import ForgotPasswordRequest


app = FastAPI()

# Inicializar base de datos al inicio
@app.on_event("startup")
def startup():
    print("Creando base de datos...")
    init_db()
    print("Base de datos lista.")


# Endpoint de prueba para insertar y obtener usuarios
app.include_router(register_routes.router)
app.include_router(login_routes.router)
app.include_router(forgot_password_routes.router)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    register = db.query(User).all()
    schema = UserJsonSchema(many=True)
    return schema.dump(register)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Define el origen de las peticiones permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los headers
)