import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class User(Model, Base):
    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255))
    last_name = Column(String(255))
    role = Column(String(255))
    identification_number = Column(String(255))
    email = Column(String(255))
    permissions = Column(Enum('develop', 'accountant', 'client', 'total'))

    def __init__(self, name, last_name, role, identification_number, email, permissions):
        Model.__init__(self)
        self.name = name
        self.last_name = last_name
        self.role = role
        self.identification_number = identification_number
        self.email = email
        self.permissions = permissions

class UserJsonSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()
    identification_number = fields.Str()
    email = fields.Str()
    permissions = fields.Str()
