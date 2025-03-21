from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.clients import Client  # Importación relativa
from ..schemas.clients_schema import ClientJsonSchema  # Importación relativa
from typing import Optional, Dict, Any

class ClientsLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_client(self, client_data: Dict[str, Any]) -> Client:
        """
        Crea un nuevo cliente en la base de datos.
        :param client_data: Diccionario con los datos del cliente.
        :return: Objeto Client creado.
        :raises ValueError: Si el cliente ya existe (por NIT o correo electrónico).
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        # Verifica si el cliente ya existe (por NIT o correo electrónico)
        existing_client = self.db.query(Client).filter(
            (Client.tax_id == client_data["tax_id"]) | (Client.email == client_data["email"])
        ).first()
        if existing_client:
            raise ValueError("El cliente ya está registrado.")

        # Crea un nuevo cliente
        new_client = Client(
            id_user=client_data["id_user"],
            name=client_data["name"],
            person_type=client_data["person_type"],
            tax_id=client_data["tax_id"],
            document_type=client_data["document_type"],
            identification_number=client_data["identification_number"],
            business_reason=client_data["business_reason"],
            email=client_data["email"],
            contact_number=client_data["contact_number"],
            address=client_data["address"],
            city=client_data["city"],
            regime_type=client_data["regime_type"],
            status=client_data.get("status", "active")  # Por defecto, el estado es "active"
        )

        try:
            self.db.add(new_client)
            self.db.commit()
            self.db.refresh(new_client)
            return new_client
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear el cliente: {e}")

    def get_client(self, client_id: str) -> Optional[Client]:
        """
        Obtiene un cliente por su ID.
        :param client_id: ID del cliente.
        :return: Objeto Client si existe, None si no se encuentra.
        """
        return self.db.query(Client).filter(Client.id == client_id).first()

    def update_client(self, client_id: str, update_data: Dict[str, Any]) -> Optional[Client]:
        """
        Actualiza los datos de un cliente existente.
        :param client_id: ID del cliente a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto Client actualizado.
        :raises ValueError: Si el cliente no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        client = self.get_client(client_id)
        if not client:
            raise ValueError("Cliente no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(client, key):
                    setattr(client, key, value)
            client.updated_at = datetime.now(timezone.utc)  # Actualiza la fecha de modificación
            self.db.commit()
            self.db.refresh(client)
            return client
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar el cliente: {e}")

    def delete_client(self, client_id: str) -> bool:
        """
        Elimina un cliente por su ID.
        :param client_id: ID del cliente a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el cliente.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        client = self.get_client(client_id)
        if not client:
            return False

        try:
            self.db.delete(client)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar el cliente: {e}")

    def get_all_clients(self) -> list:
        """
        Obtiene todos los clientes registrados.
        :return: Lista de objetos Client.
        """
        return self.db.query(Client).all()

    def get_clients_by_user(self, user_id: str) -> list:
        """
        Obtiene todos los clientes asociados a un usuario (contador).
        :param user_id: ID del usuario (contador).
        :return: Lista de objetos Client.
        """
        return self.db.query(Client).filter(Client.id_user == user_id).all()