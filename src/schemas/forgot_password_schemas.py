from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ForgotPasswordRequest(BaseModel):
    email: str
    phone:str 

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
        from_attributes = True