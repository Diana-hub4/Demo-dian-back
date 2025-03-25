from datetime import datetime, timedelta
from sqlalchemy import Column, String, Boolean, DateTime
from ..database import Base
import uuid
import secrets

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    @classmethod
    def create_token(cls, email: str, expiration_hours: int = 1):
        return cls(
            email=email,
            expires_at=datetime.utcnow() + timedelta(hours=expiration_hours)
        )

    def is_valid(self):
        return not self.used and datetime.utcnow() < self.expires_at