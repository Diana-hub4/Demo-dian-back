from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.register import Register  # Importa el modelo Register
from src.schemas.register_schema import RegisterJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash  # Para encriptar y verificar contraseñas

class RegisterLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def register_user(self, user_data: Dict[str, Any]) -> Register:
        """
        Registra un nuevo usuario en la base de datos.
        :param user_data: Diccionario con los datos del usuario.
        :return: Objeto Register creado.
        :raises ValueError: Si el correo electrónico ya está registrado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        # Verifica si el correo electrónico ya está registrado
        existing_user = self.db.query(Register).filter(Register.email == user_data["email"]).first()
        if existing_user:
            raise ValueError("El correo electrónico ya está registrado.")

        # Crea un nuevo usuario
        new_user = Register(
            name=user_data["name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            identification_number=user_data["identification_number"],
            email=user_data["email"],
            permissions=user_data["permissions"],
            password=user_data["password"]
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al registrar el usuario: {e}")

    def authenticate_user(self, email: str, password: str) -> Optional[Register]:
        """
        Autentica a un usuario verificando su correo electrónico y contraseña.
        :param email: Correo electrónico del usuario.
        :param password: Contraseña del usuario.
        :return: Objeto Register si las credenciales son válidas, None si no lo son.
        """
        user = self.db.query(Register).filter(Register.email == email).first()  # Busca al usuario por correo electrónico
        if user and user.check_password(password):  # Verifica la contraseña
            return user
        return None

    def get_user_by_email(self, email: str) -> Optional[Register]:
        """
        Obtiene un usuario por su correo electrónico.
        :param email: Correo electrónico del usuario.
        :return: Objeto Register si existe, None si no se encuentra.
        """
        return self.db.query(Register).filter(Register.email == email).first()

    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Register]:
        """
        Actualiza los datos de un usuario existente.
        :param user_id: ID del usuario a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto Register actualizado.
        :raises ValueError: Si el usuario no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        user = self.db.query(Register).filter(Register.id == user_id).first()
        if not user:
            raise ValueError("Usuario no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar el usuario: {e}")

    def delete_user(self, user_id: str) -> bool:
        """
        Elimina un usuario por su ID.
        :param user_id: ID del usuario a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el usuario.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        user = self.db.query(Register).filter(Register.id == user_id).first()
        if not user:
            return False

        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar el usuario: {e}")