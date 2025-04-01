import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.schemas.register_schema import UserJsonSchema
from .model import Model, Base
from marshmallow import Schema, fields
from src.models.register import User
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore # Para manejar contraseñas seguras

# Tabla para registrar los inicios de sesión (ya existente)
class Login(Model, Base):
    __tablename__ = 'login'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)
    email = Column(String(50),nullable=False)
    login_date = Column(DateTime)

    def __init__(self, id_user, email, login_date):
        Model.__init__(self)
        self.id_user = id_user
        self.email=email
        self.login_date = login_date

# Esquema para serializar/deserializar la tabla User
class UserSchema(Schema):
    id = fields.Str()
    email = fields.Str()
    password_hash = fields.Str()

# Esquema para serializar/deserializar la tabla Login (ya existente)
class LoginJsonSchema(Schema):
    id = fields.Str()
    id_user = fields.Str()
    email = fields.Str()
    login_date = fields.DateTime()

# Función para autenticar al usuario
def authenticate_user(email, password,db):
    """
    Autentica a un usuario verificando su correo electrónico y contraseña.
    Retorna el objeto User si las credenciales son válidas, de lo contrario retorna None.
    """
    try: 
        user = db.query(User).filter_by(email=email).first() 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    if user and user.check_password(password):  # Verifica la contraseña
        return user
    return None

# Función para registrar un nuevo inicio de sesión
def register_login(user_id, user_email):
    """
    Registra un nuevo inicio de sesión en la tabla login.
    """
    new_login = Login(id_user=user_id, email=user_email, login_date=datetime.now(timezone.utc))
    return new_login
