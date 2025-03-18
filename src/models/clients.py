import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class Client(Model, Base):
    __tablename__ = 'clients'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)
    name = Column(String(255))
    person_type = Column(Enum('Natural', 'Legal', 'Company'))
    tax_id = Column(String(255))
    document_type = Column(Enum('id_card', 'foreign_id', 'other'))
    identification_number = Column(String(255))
    status = Column(Enum('active', 'inactive'))

    def __init__(self, id_user, name, person_type, tax_id, document_type, identification_number, status):
        Model.__init__(self)
        self.id_user = id_user
        self.name = name
        self.person_type = person_type
        self.tax_id = tax_id
        self.document_type = document_type
        self.identification_number = identification_number
        self.status = status

class ClientJsonSchema(Schema):
    id = fields.Str()
    id_user = fields.Str()
    name = fields.Str()
    person_type = fields.Str()
    tax_id = fields.Str()
    document_type = fields.Str()
    identification_number = fields.Str()
    status = fields.Str()
