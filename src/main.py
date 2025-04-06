from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from src.database import init_db
from src.routes import (
    pqrsf_routes,
    register_routes,
    login_routes,
    forgot_password_routes
)

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de la base de datos
@app.on_event("startup")
async def startup_event():
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos lista.")

# Incluir routers
app.include_router(pqrsf_routes.router)
app.include_router(register_routes.router)
app.include_router(login_routes.router)
app.include_router(forgot_password_routes.router)

# Ruta principal
@app.get("/")
def read_root():
    return {"message": "Sistema DIAN - Backend"}

# Ruta para descargar guía
PDF_PATH = os.path.join(os.path.dirname(__file__), "public", "assets", "Guía Completa del Sistema de Contabilidad DIAN-Colombia.pdf")

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