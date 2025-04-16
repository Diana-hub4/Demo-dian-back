## src\models\register.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.orm import Session, relationship 
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv  
import os
from typing import Optional, Dict, Any
from src.database import Base
from src.models.base import Model


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "Diana_Sar")  
class User(Base):
    """Modelo de usuario para el sistema de contabilidad."""
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)   
    role = Column(String(255), nullable=False)
    identification_number = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    permissions = Column(Enum('develop', 'accountant', 'client', 'total', name='permissions_enum'), nullable=False)
    password_hash = Column(String(128), nullable=False)
    status = Column(Enum('activo', 'inactivo', 'pendiente', name='status_enum'),nullable=False, default='pendiente')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))
    
    logins = relationship("Login", back_populates="user")

    def __init__(self, **kwargs):
        super().__init__()
        self.first_name = kwargs.get('first_name') 
        self.last_name = kwargs.get('last_name')
        self.role = kwargs.get('role')
        self.identification_number = kwargs.get('identification_number')
        self.email = kwargs.get('email')
        self.permissions = kwargs.get('permissions')
        self.status = kwargs.get('status', 'pendiente')
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def set_password(self, password: str) -> None:
        """Encripta y establece la contraseña del usuario."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_email(cls, session: Session, email: str) -> Optional['User']:
        """Obtiene un usuario por su email."""
        return session.query(cls).filter(cls.email == email).first()

    @classmethod
    def create(cls, session: Session, user_data: Dict[str, Any]) -> 'User':
        """Crea un nuevo usuario en la base de datos."""
        user = cls(**user_data)
        session.add(user)
        session.commit()
        return user

    def update(self, session: Session, **kwargs) -> None:
        """Actualiza los datos del usuario."""
        for key, value in kwargs.items():
            if key == 'password':
                self.set_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
        session.commit()

    def to_dict(self) -> Dict[str, Any]:
        """Devuelve un diccionario con los datos del usuario (sin la contraseña)."""
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'role': self.role,
            'identification_number': self.identification_number,
            'email': self.email,
            'permissions': self.permissions,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }