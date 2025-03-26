from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.forgot_password_schemas import ForgotPasswordRequest, ResetPasswordRequest  # Import absoluto
from src.business_logic.forgot_password_logic import request_password_reset, reset_password  # Import absoluto
from src.database import get_db  # Import absoluto
from src.utils.exceptions import handle_exceptions  # Import absoluto

router = APIRouter()

@router.post("/forgot-password")
@handle_exceptions
def forgot_password(
    request: ForgotPasswordRequest, 
    db: Session = Depends(get_db)
):
   return {"message": f"Email recibido: {request.email}"}

@router.post("/reset-password")
@handle_exceptions
def reset_password_endpoint(
    request: ResetPasswordRequest, 
    db: Session = Depends(get_db)
):
    """
    Restablece la contraseña usando un token válido.
    """
    result = reset_password(db, request)
    return result