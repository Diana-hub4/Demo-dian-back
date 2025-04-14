from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import sqlite3
from typing import Optional
from src.database import Base, engine
from pydantic import BaseModel
from src.models.register import User 
from src.database import init_db
from src.routes import (
    pqrsf_routes,
    register_routes,
    login_routes,
    forgot_password_routes,
    auth_routes
)

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente")

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class LoginRequest(BaseModel):
    email: str
    password: str

# Configuración para archivos estáticos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Inicialización de la base de datos
@app.on_event("startup")
async def startup_event():
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos lista.")

    # Crear directorio para uploads si no existe
    os.makedirs("uploads", exist_ok=True)
    
    # Inicializar conexión a SQLite para nóminas
    init_nominas_db()

def init_nominas_db():
    """Inicializa la base de datos SQLite para nóminas"""
    conn = sqlite3.connect("HANA.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nominas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_contrato TEXT NOT NULL,
            periodo TEXT NOT NULL,
            colaborador TEXT NOT NULL,
            salario REAL NOT NULL,
            deducciones REAL NOT NULL,
            correo TEXT NOT NULL,
            aportes REAL NOT NULL,
            documento_nombre TEXT,
            total_bruto REAL NOT NULL,
            total_neto REAL NOT NULL,
            fecha_creacion TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Tabla de nóminas creada correctamente en HANA.db")

# Incluir routers
app.include_router(pqrsf_routes.router)
app.include_router(register_routes.router)
app.include_router(login_routes.router)
app.include_router(forgot_password_routes.router)
app.include_router(auth_routes.router)

# Ruta principal
@app.get("/")
def read_root():
    return {"message": "Sistema DIAN - Backend"}

# Ruta para descargar guía
PDF_PATH = os.path.join(
    os.path.dirname(__file__), "public", "assets", "Guía Completa del Sistema de Contabilidad DIAN-Colombia.pdf")

@app.get("/descargar-guia")
async def descargar_guia():
    if not os.path.exists(PDF_PATH):
        raise HTTPException(
            status_code=404,
            detail="El archivo de la guía no se encuentra disponible temporalmente"
        )
    
    return FileResponse(
        path=PDF_PATH,
        filename="Guia_Contable_DIAN.pdf",
        media_type="application/pdf"
    )

@app.post("/login")
def login_user(request: LoginRequest):
    # Aquí iría tu lógica para validar el usuario
    return {"message": "Login successful"}

# Endpoint para nóminas
@app.post("/api/nominas")
async def crear_nomina(
    tipoContrato: str = Form(...),
    periodo: str = Form(...),
    colaborador: str = Form(...),
    salario: float = Form(...),
    deducciones: float = Form(...),
    correo: str = Form(...),
    aportes: float = Form(...),
    totalBruto: float = Form(...),
    totalNeto: float = Form(...),
    documento: Optional[UploadFile] = File(None)
):
    try:
        conn = sqlite3.connect("HANA.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        documento_nombre = documento.filename if documento else None
        
        cursor.execute('''
            INSERT INTO nominas (
                tipo_contrato, periodo, colaborador, salario, 
                deducciones, correo, aportes, documento_nombre,
                total_bruto, total_neto, fecha_creacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tipoContrato,
            periodo,
            colaborador,
            salario,
            deducciones,
            correo,
            aportes,
            documento_nombre,
            totalBruto,
            totalNeto,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        nomina_id = cursor.lastrowid
        conn.close()
        
        # Si hay documento, guardarlo en el sistema de archivos
        if documento:
            file_location = f"uploads/{documento.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await documento.read())
        
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "id": nomina_id,
                "message": "Nómina creada exitosamente",
                "documento_url": f"/uploads/{documento.filename}" if documento else None
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)