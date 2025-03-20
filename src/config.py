# src/config.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    # Configuración de Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Servidor SMTP
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Puerto SMTP
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']  # Usar TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'tu_correo@gmail.com')  # Correo electrónico
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'tu_contraseña')  # Contraseña del correo
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'tu_correo@gmail.com')  # Correo remitente