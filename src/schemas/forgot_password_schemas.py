from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PasswordResetToken(BaseModel):
    id: str
    email: str
    token: str
    expires_at: datetime
    used: bool = False

    class Config:
        orm_mode = True