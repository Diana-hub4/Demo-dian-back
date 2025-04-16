## src\config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings 
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    # Configuración de base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    # Configuración de autenticación
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key-default")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 7,  # 7 días
        alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )

    # Configuración de email
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    SENDGRID_TEMPLATE_ID: str = os.getenv("SENDGRID_TEMPLATE_ID", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:4200")
    
    # Configuración SMTP
    MAIL_SERVER: str = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER: str = os.getenv('MAIL_DEFAULT_SENDER', '')

    class Config:
        env_file = ".env"
        extra = "ignore"  # Permite ignorar variables extra no definidas
        validate_by_name = True  # Permite usar alias

settings = Settings()