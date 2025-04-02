# src/config.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class Settings:
    def __init__(self):
        # Configuración de SendGrid
        self.SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
        self.EMAIL_FROM = os.getenv("EMAIL_FROM") 
        self.SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")

        # Configuración de autenticación
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-default")
        self.ALGORITHM = "HS256"

        # Validación de configuraciones esenciales
        if None in [self.SENDGRID_API_KEY, self.EMAIL_FROM, self.SENDGRID_TEMPLATE_ID]:
            raise ValueError("Faltan configuraciones esenciales en .env")
class Config:
    # Configuración de Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Servidor SMTP
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Puerto SMTP
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']  # Usar TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'tu_correo@gmail.com')  # Correo electrónico
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'tu_contraseña')  # Contraseña del correo
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'tu_correo@gmail.com')  # Correo remitente

settings = Settings()
config = Config() 
