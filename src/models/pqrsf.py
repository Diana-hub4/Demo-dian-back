# src/models/pqrsf.py
import uuid
import os
import shutil
from sqlalchemy import Column, Integer, String, DateTime, JSON
from .model import Model, Base
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from src.database import Base

class PQRSF(Base):
    __tablename__ = "pqrsf"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_radicado = Column(String(36), unique=True, index=True)
    tipo = Column(String) 
    mensaje = Column(String)
    archivos = Column(JSON)  # Lista de nombres de archivos
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")
    respuesta = Column(String, nullable=True) 
    email_usuario = Column(String)
