# src/main.py
from fastapi import FastAPI
from .routes import paymentsTransfers_routes

app = FastAPI()

# Registrar las rutas de paymentsTransfers
app.include_router(paymentsTransfers_routes.router, prefix="/api")