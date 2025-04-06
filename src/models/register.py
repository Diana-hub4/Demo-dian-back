import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime
from .model import Model, Base
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore # Para encriptar y verificar contraseñas
from dotenv import load_dotenv  # type: ignore # Para cargar variables de entorno
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Palabra secreta para encriptar (puedes quemarla o traerla de .env)
SECRET_KEY = os.getenv("SECRET_KEY", "Diana_Sar")  # Usa una palabra secreta por defecto si no hay .env

class User(Model, Base):
    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)  # Nombre del usuario
    last_name = Column(String(255), nullable=False)  # Apellido del usuario
    role = Column(String(255), nullable=False)  # Cargo o rol del usuario
    identification_number = Column(String(255), nullable=False)  # Cédula o NIT
    email = Column(String(255), unique=True, nullable=False)  # Correo electrónico único
    permissions = Column(Enum('develop', 'accountant', 'client', 'total'), nullable=False)  # Permisos del usuario
    password = Column(String(128), nullable=False)  # Contraseña encriptada
    status= Column(Enum('activo','inactivo','pendiente'),nullable=False) # Estado del usuario.

    def __init__(self, name, last_name, role, identification_number, email, permissions, password, status):
        Model.__init__(self)
        self.name = name
        self.last_name = last_name
        self.role = role
        self.identification_number = identification_number
        self.email = email
        self.permissions = permissions
        self.set_password(password)  # Encripta la contraseña al crear el usuario
        self.status = status

    def set_password(self, password):
        """Encripta la contraseña y la almacena en el campo password_hash."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return check_password_hash(self.password, password)

# Esquema para serializar/deserializar la tabla Register
class UserJsonSchema(Model, Base):
    id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()
    identification_number = fields.Str()
    email = fields.Str()
    permissions = fields.Str()
    password = fields.Str(load_only=True)
    status = fields.Str()  # Solo para recibir datos, no se incluye en la salida

# Función para registrar un nuevo usuario
def register_user(name, last_name, role, identification_number, email, permissions, password,status):
    """
    Registra un nuevo usuario en la tabla register.
    Retorna el objeto Register si el registro es exitoso.
    """
    # Verifica si el correo electrónico ya está registrado
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ValueError("El correo electrónico ya está registrado.")

    # Crea un nuevo registro
    new_user = User(
        name=name,
        last_name=last_name,
        role=role,
        identification_number=identification_number,
        email=email,
        permissions=permissions,
        password=password,
        status=status
    )
    return new_user

