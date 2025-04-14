from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class LoginRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    password: str
    
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True 