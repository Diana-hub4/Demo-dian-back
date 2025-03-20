# src/__init__.py

from flask import Flask
from flask_mail import Mail

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar configuraciones desde config.py
app.config.from_object('src.config.Config')

# Inicializar Flask-Mail
mail = Mail(app)

# Importar rutas (esto debe ir al final para evitar importaciones circulares)
from src.routes import *