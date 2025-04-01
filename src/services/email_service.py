
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import settings

async def send_password_reset_email(email: str, token: str, phone: str = None):
    
    try:
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        message = Mail(
            from_email=settings.EMAIL_FROM,
            to_emails=email,
            subject="Restablecer tu contraseña",
            html_content=f"""
            <h2>Hola {user_name}</h2>
            <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
            <p>Haz clic en el siguiente enlace para continuar:</p>
            <a href="{http://localhost:4200/reset-password}">{reset_url}</a>
            <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
            <p>El enlace expirará en 1 hora.</p>
            """
        )
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
        raise Exception(f"Error enviando email: {str(e)}")