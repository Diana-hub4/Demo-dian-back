from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from ..schemas.auth_schemas import Token
from src.services.auth_service import authenticate_user, create_access_token, get_password_hash
from ..utils.security import create_access_token
from datetime import timedelta, datetime
from ..config import settings
from src.schemas.auth_schemas import LoginRequest, Token
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.register import User
import jwt



router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends (get_db)
    ):

    user = authenticate_user(db, login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
        }
    }

async def get_token_from_header(authorization: str = Header(..., description="Token en formato Bearer")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de autorización inválido. Use 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ")[1]

async def verify_token(token: str = Depends(get_token_from_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise credentials_exception

@router.get("/verify")
async def verify_token_endpoint(
    current_user: dict = Depends(verify_token), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == current_user.get("sub")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {
        "is_valid": True,
        "user_info": {
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}",
        }
    }