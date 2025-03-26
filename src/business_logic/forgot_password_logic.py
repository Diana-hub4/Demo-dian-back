from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import secrets
from src.models.forgot_password import PasswordResetToken  # Import absoluto
from src.models.register import Register
from src.schemas.forgot_password_schemas import ForgotPasswordRequest, ResetPasswordRequest  # Import absoluto
from src.models.login import User  # Import absoluto
from src.services.email_service import send_password_reset_email  # Import absoluto
from src.utils.exceptions import NotFoundException, InvalidTokenException  # Import absoluto
from src.utils.auth import create_access_token, verify_token
from src.config import settings

def reset_password(db: Session, request: ResetPasswordRequest):
    # Verificar si el token es válido y no ha expirado
    token_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not token_record:
        raise InvalidTokenException("Token inválido o expirado")
    
def request_password_reset(db: Session, request: ForgotPasswordRequest):
    # Verificar si el usuario existe
    user = db.query(Register).filter(Register.email == request.email).first()
    if not user:
        return
    
    # Invalidar tokens previos para este email
    db.query(PasswordResetToken).filter(
        PasswordResetToken.email == request.email,
        PasswordResetToken.used == False
    ).update({"used": True})
    
    # Crear nuevo token
    token_data = {"sub": user.email, "type": "password_reset"}
    jwt_token = create_access_token(data=token_data)

    reset_token = PasswordResetToken(
        email=user.email,
        token=jwt_token,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    db.add(reset_token)
    db.commit()
    
    send_password_reset_email(email=user.email, token=jwt_token)
    
    return {"message": "Email de recuperación enviado"}    

