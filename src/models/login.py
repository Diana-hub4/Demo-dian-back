import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from .model import Model, Base
from marshmallow import Schema, fields


class Login(Model, Base):
    __tablename__ = 'login'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = Column(String(36), ForeignKey('user.id'), nullable=False)
    login_date = Column(DateTime)

    def __init__(self, id_user, login_date):
        Model.__init__(self)
        self.id_user = id_user
        self.login_date = login_date

class LoginJsonSchema(Schema):
    id = fields.Str()
    id_user = fields.Str()
    login_date = fields.DateTime()
