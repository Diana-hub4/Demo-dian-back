from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.register import User
from src.schemas.forgot_password_schemas import ForgotPasswordRequest, ResetPasswordRequest  # Import absoluto
from src.business_logic.forgot_password_logic import request_password_reset, reset_password  # Import absoluto
from src.database import get_db  
from src.services.email_service import send_password_reset_email
from src.utils.auth import create_reset_token
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest,db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return {"message": f"Si el email {request.email} existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña."}
    
    reset_token = create_reset_token(user.email)
    
    try:
        await send_password_reset_email(
            email=user.email,
            token=reset_token,
            user_name=user.name
        )
        return {"message": "Correo enviado exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar el correo: {str(e)}"
        )

    except Exception as e:  # Añadido bloque except
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar el correo: {str(e)}"
        )

@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPasswordRequest, 
    db: Session = Depends(get_db)
):
    """
    Restablece la contraseña usando un token válido.
    """
    result = reset_password(db, request)
    return result

