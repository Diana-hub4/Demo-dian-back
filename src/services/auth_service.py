from ..models.user import User
from ..utils.security import verify_password

def authenticate_user(email: str, password: str):
    user = User.get_by_email(email)  # Asume que tienes este método en tu modelo
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user