
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..config import settings
def send_password_reset_email(email: str, token: str):
    print(f"Enviando email a {email}")
    print(f"Token: {token}")
    print(f"API Key: {settings.SENDGRID_API_KEY}")
    print(f"Email From: {settings.EMAIL_FROM}")
    print(f"Frontend URL: {settings.FRONTEND_URL}")
    print(f"Access Token Expire Minutes: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=email,
        subject="Restablecer tu contraseña",
        html_content=f"""
        <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
        <p>Haz clic en el siguiente enlace para continuar:</p>
        <a href="{reset_url}">{reset_url}</a>
        <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
        <p>El enlace expirará en 1 hora.</p>
        """
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)  # Inicializa el cliente
        response = sg.send(message)  # Llama al método correcto
        return response
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
        raise