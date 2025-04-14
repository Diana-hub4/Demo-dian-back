# src/models/base.py
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from src.database import Base

class Model(Base):
    """Clase base abstracta para todos los modelos"""
    __abstract__ = True  # Esto hace que SQLAlchemy no cree tabla para esta clase
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), 
                       onupdate=lambda: datetime.now(timezone.utc))

class ModelBase(Base):
    __abstract__ = True  # Hace que SQLAlchemy ignore esta clase para tablas
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), 
                      onupdate=lambda: datetime.now(timezone.utc))
    
