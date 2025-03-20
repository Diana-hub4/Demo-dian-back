import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime
from .model import Model
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore # Para encriptar y verificar contraseñas
from dotenv import load_dotenv  # type: ignore # Para cargar variables de entorno
import os
from .base import Base  # Importar Base desde base.py

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Palabra secreta para encriptar (puedes quemarla o traerla de .env)
SECRET_KEY = os.getenv("SECRET_KEY", "mi_palabra_secreta")  # Usa una palabra secreta por defecto si no hay .env

# Tabla para almacenar la información del usuario (registro)
class Register(Base):
    __tablename__ = 'register'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)  # Nombre del usuario
    last_name = Column(String(255), nullable=False)  # Apellido del usuario
    role = Column(String(255), nullable=False)  # Cargo o rol del usuario
    identification_number = Column(String(255), nullable=False)  # Cédula o NIT
    email = Column(String(255), unique=True, nullable=False)  # Correo electrónico único
    permissions = Column(Enum('develop', 'accountant', 'client', 'total'), nullable=False)  # Permisos del usuario
    password_hash = Column(String(128), nullable=False)  # Contraseña encriptada
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  # Fecha de creación del registro

    def __init__(self, name, last_name, role, identification_number, email, permissions, password):
        Model.__init__(self)
        self.name = name
        self.last_name = last_name
        self.role = role
        self.identification_number = identification_number
        self.email = email
        self.permissions = permissions
        self.set_password(password)  # Encripta la contraseña al crear el usuario

    def set_password(self, password):
        """Encripta la contraseña y la almacena en el campo password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return check_password_hash(self.password_hash, password)

# Esquema para serializar/deserializar la tabla Register
class RegisterJsonSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()
    identification_number = fields.Str()
    email = fields.Str()
    permissions = fields.Str()
    password = fields.Str(load_only=True)  # Solo para recibir datos, no se incluye en la salida
    created_at = fields.DateTime()

# Función para registrar un nuevo usuario
def register_user(name, last_name, role, identification_number, email, permissions, password):
    """
    Registra un nuevo usuario en la tabla register.
    Retorna el objeto Register si el registro es exitoso.
    """
    # Verifica si el correo electrónico ya está registrado
    existing_user = Register.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError("El correo electrónico ya está registrado.")

    # Crea un nuevo registro
    new_user = Register(
        name=name,
        last_name=last_name,
        role=role,
        identification_number=identification_number,
        email=email,
        permissions=permissions,
        password=password
    )
    return new_user

# Función para autenticar un usuario
def authenticate_user(email, password):
    """
    Autentica a un usuario verificando su correo electrónico y contraseña.
    Retorna el objeto Register si las credenciales son válidas, de lo contrario retorna None.
    """
    user = Register.query.filter_by(email=email).first()  # Busca al usuario por correo electrónico
    if user and user.check_password(password):  # Verifica la contraseña
        return user
    return None