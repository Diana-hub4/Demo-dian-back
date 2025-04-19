from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.login import User, Login  # Importa los modelos User y Login
from src.schemas.login_schema import UserSchema, LoginJsonSchema  # Importa los esquemas para serialización
from typing import Optional, Dict, Any

class LoginLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def register_login(self, user_id: str) -> Login:
        """
        Registra un nuevo inicio de sesión en la tabla login.
        :param user_id: ID del usuario que inició sesión.
        :return: Objeto Login creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_login = Login(id_user=user_id, login_date=datetime.now(timezone.utc))

        try:
            self.db.add(new_login)
            self.db.commit()
            self.db.refresh(new_login)
            return new_login
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al registrar el inicio de sesión: {e}")

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.
        :param email: Correo electrónico del usuario.
        :return: Objeto User si existe, None si no se encuentra.
        """
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        Crea un nuevo usuario en la base de datos.
        :param user_data: Diccionario con los datos del usuario (email y password).
        :return: Objeto User creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_user = User(email=user_data["email"], password=user_data["password"])

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear el usuario: {e}")

    def update_password(self, user_id: str, new_password: str) -> Optional[User]:
        """
        Actualiza la contraseña de un usuario.
        :param user_id: ID del usuario.
        :param new_password: Nueva contraseña.
        :return: Objeto User actualizado.
        :raises ValueError: Si el usuario no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Usuario no encontrado.")

        try:
            user.set_password(new_password)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar la contraseña: {e}")

    def get_terms_and_conditions(self) -> Dict[str, Any]:
        """
        Retorna los términos y condiciones.
        :return: Diccionario con los términos y condiciones.
        """
        # Simulación de términos y condiciones
        terms_and_conditions = {
            "title": "Términos y Condiciones",
            "content": "Aquí van los términos y condiciones del servicio..."
        }
        return terms_and_conditions