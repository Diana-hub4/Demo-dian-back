# from flask import request, jsonify, url_for
# from src import app, mail
# from flask_mail import Message
# from itsdangerous import URLSafeTimedSerializer
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from src.database import SessionSql, get_db
# from src.models import User
# from src.schemas import UserJsonSchema
# from src.models.register import Register

# # Configuración del serializer para tokens
# SECRET_KEY = "Diana_Sar"  # Debe ser la misma que usas en la encriptación de contraseñas
# serializer = URLSafeTimedSerializer(SECRET_KEY)

# # Router de FastAPI para los endpoints de usuarios
# router = APIRouter()

# # Endpoint para recuperar contraseña (Flask)
# @app.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     data = request.get_json()
#     email = data.get('email')

#     # Verificar si el usuario existe
#     user = Register.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({"message": "Correo electrónico no registrado"}), 404

#     # Generar token
#     token = serializer.dumps(email, salt='password-reset-salt')

#     # Crear el enlace de recuperación
#     reset_url = url_for('reset_password', token=token, _external=True)

#     # Enviar correo electrónico
#     msg = Message(
#         subject="Recuperación de Contraseña",
#         recipients=[email],
#         body=f"Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}"
#     )
#     mail.send(msg)

#     return jsonify({"message": "Correo de recuperación enviado"}), 200

# # Endpoint para restablecer contraseña (Flask)
# @app.route('/reset-password/<token>', methods=['POST'])
# def reset_password(token):
#     data = request.get_json()
#     new_password = data.get('new_password')

#     # Validar el token
#     try:
#         email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # Token válido por 1 hora
#     except:
#         return jsonify({"message": "Token inválido o expirado"}), 400

#     # Obtener la sesión de la base de datos
#     db = SessionSql()
    
#     # Buscar al usuario
#     user = db.query(Register).filter(Register.email == email).first()
#     if not user:
#         db.close()  # Cerrar la sesión si el usuario no existe
#         return jsonify({"message": "Usuario no encontrado"}), 404
    

#     # Cambiar la contraseña
#     user.set_password(new_password)

#     db.commit()
#     db.close()  # Cerrar la sesión después de usarla

#     return jsonify({"message": "Contraseña actualizada correctamente"}), 200

# # Incluir el router de FastAPI en la aplicación Flask
# app.include_router(router)