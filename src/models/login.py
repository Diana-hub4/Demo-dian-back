import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .model import Model, Base
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore # Para manejar contraseñas seguras

# Tabla para almacenar la información del usuario (correo electrónico y contraseña)
class User(Model, Base):
    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(100), unique=True, nullable=False)  # Correo electrónico único
    password_hash = Column(String(128), nullable=False)  # Contraseña encriptada

    # Relación con la tabla de login (un usuario puede tener muchos inicios de sesión)
    logins = relationship('Login', backref='user')

    def __init__(self, email, password):
        Model.__init__(self)
        self.email = email
        self.set_password(password)  # Encripta la contraseña al crear el usuario

    def set_password(self, password):
        """Encripta la contraseña y la almacena en el campo password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return check_password_hash(self.password_hash, password)

# Tabla para registrar los inicios de sesión (ya existente)
class Login(Model, Base):
    __tablename__ = 'login'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)
    login_date = Column(DateTime)

    def __init__(self, id_user, login_date):
        Model.__init__(self)
        self.id_user = id_user
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
    login_date = fields.DateTime()

# Función para autenticar al usuario
def authenticate_user(email, password):
    """
    Autentica a un usuario verificando su correo electrónico y contraseña.
    Retorna el objeto User si las credenciales son válidas, de lo contrario retorna None.
    """
    user = User.query.filter_by(email=email).first()  # Busca al usuario por correo electrónico
    if user and user.check_password(password):  # Verifica la contraseña
        return user
    return None

# Función para registrar un nuevo inicio de sesión
def register_login(user_id):
    """
    Registra un nuevo inicio de sesión en la tabla login.
    """
    new_login = Login(id_user=user_id, login_date=datetime.now(timezone.utc))
    return new_login
