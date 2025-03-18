import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields

class DianVerification(Model, Base):
    __tablename__ = 'dian_verification'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_generator = Column(String(36), ForeignKey('generator.id'), nullable=False)
    requirements_check = Column(String(5))
    copy_sent_to_client = Column(String(5))

    def __init__(self, id_generator, requirements_check, copy_sent_to_client):
        Model.__init__(self)
        self.id_generator = id_generator
        self.requirements_check = requirements_check
        self.copy_sent_to_client = copy_sent_to_client

class DianVerificationJsonSchema(Schema):
    id = fields.Str()
    id_generator = fields.Str()
    requirements_check = fields.Str()
    copy_sent_to_client = fields.Str()
