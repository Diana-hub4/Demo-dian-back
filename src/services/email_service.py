
from http.client import HTTPException
import sendgrid
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import settings
from fastapi import HTTPException

async def send_password_reset_email(email: str, token: str, user_name: str):

    if not all([settings.EMAIL_FROM, settings.SENDGRID_TEMPLATE_ID]):
        raise HTTPException(
            status_code=500,
            detail="Configuración de email incompleta"
        )

    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}" 
    print(f"Enviando a: {email}")
    print(f"Template ID: {settings.SENDGRID_TEMPLATE_ID}")
    print(f"From: {settings.EMAIL_FROM}")
    message = {
        "from": {
            "email": settings.EMAIL_FROM,
            "name": "Soporte Sistema Contable"
        },
        "personalizations": [
            {
                "to": [{"email": email, "name": user_name}],
                "dynamic_template_data": {
                    "nombre_usuario": user_name,
                    "reset_link": reset_url
                }
            }
        ],
        "template_id": settings.SENDGRID_TEMPLATE_ID  
    }
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=message)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.body}")
        print(f"Headers: {response.headers}")

        if response.status_code >= 400:
            raise HTTPException(
                status_code=500,
                detail=f"Error de SendGrid: {response.body.decode('utf-8')}"
            )
        
        return {"status": response.status_code, "message": "Email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando email: {str(e)}"
        )