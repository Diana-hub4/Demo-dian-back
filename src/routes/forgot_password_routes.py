from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.forgot_password_schemas import ForgotPasswordRequest, ResetPasswordRequest  # Import absoluto
from src.business_logic.forgot_password_logic import request_password_reset, reset_password  # Import absoluto
from src.database import get_db  # Import absoluto
from src.utils.exceptions import handle_exceptions  # Import absoluto

router = APIRouter(tags=["Password Recovery"])

@router.post("/forgot-password")
@handle_exceptions
async def forgot_password(
    request: ForgotPasswordRequest, 
    db: Session = Depends(get_db)
):
    """
    Solicita un enlace para restablecer la contraseña.
    Siempre devuelve 200 para no revelar si el email existe o no.
    """
    request_password_reset(db, request)
    return {"message": "Si el email existe, se ha enviado un enlace para restablecer la contraseña"}

@router.post("/reset-password")
@handle_exceptions
async def reset_password_endpoint(
    request: ResetPasswordRequest, 
    db: Session = Depends(get_db)
):
    """
    Restablece la contraseña usando un token válido.
    """
    result = reset_password(db, request)
    return result