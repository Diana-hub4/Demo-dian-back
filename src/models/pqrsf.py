# src/models/pqrsf.py
import uuid
from sqlalchemy import Column, String, Text, DateTime
from .model import Model, Base
from datetime import datetime

class PQRSF(Base):
    __tablename__ = 'pqrsf'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pqrsf_type = Column(String(50), nullable=False)  # Tipo de PQRSF
    message = Column(Text, nullable=False)          # Mensaje de la solicitud
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación

    def __init__(self, pqrsf_type, message):
        self.pqrsf_type = pqrsf_type
        self.message = message