import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session 
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from src.models.base import Model
from marshmallow import Schema, fields
from src.models.register import User

class Login(Model, Base):
    __tablename__ = 'login'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('users.id'), nullable=False)
    email = Column(String(50),nullable=False)
    login_date = Column(DateTime)

    user = relationship("User", back_populates="logins")

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
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verify_password(password):
        return None
    return user
    
# Función para registrar un nuevo inicio de sesión
def register_login(db: Session, user_id: str, email: str, name: str = None, identification: str = None):
    new_login = Login(
        id_user=user_id,
        email=email,
        name=name,
        identification=identification,
        login_date=datetime.now(timezone.utc)
    )
    db.add(new_login)
    db.commit()
    return new_login