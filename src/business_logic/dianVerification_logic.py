from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.dianVerification import DianVerification  # Importación relativa
from ..schemas.dianVerification_schema import DianVerificationJsonSchema  # Importación relativa
from typing import Optional, Dict, Any

class DianVerificationLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_verification(self, verification_data: Dict[str, Any]) -> DianVerification:
        """
        Crea un nuevo registro de verificación DIAN.
        :param verification_data: Diccionario con los datos de verificación.
        :return: Objeto DianVerification creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_verification = DianVerification(
            id_generator=verification_data["id_generator"],
            requirements_check=verification_data.get("requirements_check", "No"),  # Por defecto, "No"
            copy_sent_to_client=verification_data.get("copy_sent_to_client", "No")  # Por defecto, "No"
        )

        try:
            self.db.add(new_verification)
            self.db.commit()
            self.db.refresh(new_verification)
            return new_verification
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear la verificación DIAN: {e}")

    def get_verification(self, verification_id: str) -> Optional[DianVerification]:
        """
        Obtiene una verificación DIAN por su ID.
        :param verification_id: ID de la verificación.
        :return: Objeto DianVerification si existe, None si no se encuentra.
        """
        return self.db.query(DianVerification).filter(DianVerification.id == verification_id).first()

    def update_verification(self, verification_id: str, update_data: Dict[str, Any]) -> Optional[DianVerification]:
        """
        Actualiza los datos de una verificación DIAN existente.
        :param verification_id: ID de la verificación a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto DianVerification actualizado.
        :raises ValueError: Si la verificación no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        verification = self.get_verification(verification_id)
        if not verification:
            raise ValueError("Verificación DIAN no encontrada.")

        try:
            for key, value in update_data.items():
                if hasattr(verification, key):
                    setattr(verification, key, value)
            self.db.commit()
            self.db.refresh(verification)
            return verification
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar la verificación DIAN: {e}")

    def delete_verification(self, verification_id: str) -> bool:
        """
        Elimina una verificación DIAN por su ID.
        :param verification_id: ID de la verificación a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró la verificación.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        verification = self.get_verification(verification_id)
        if not verification:
            return False

        try:
            self.db.delete(verification)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar la verificación DIAN: {e}")

    def verify_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica un documento (factura electrónica) con la DIAN.
        :param document_data: Diccionario con los datos del documento a verificar.
        :return: Respuesta de la DIAN con el estado de verificación.
        """
        # Simulación de envío a la DIAN y respuesta
        # En un entorno real, aquí se haría una solicitud HTTP a la API de la DIAN
        dian_response = {
            "status": "success",
            "message": "Documento verificado exitosamente",
            "requirements_check": "Yes",  # Supongamos que cumple con los requisitos
            "copy_sent_to_client": "Yes"  # Supongamos que se envió una copia al cliente
        }

        # Guardar la respuesta en la base de datos
        verification_data = {
            "id_generator": document_data.get("id_generator"),
            "requirements_check": dian_response.get("requirements_check", "No"),
            "copy_sent_to_client": dian_response.get("copy_sent_to_client", "No")
        }
        self.create_verification(verification_data)

        return dian_response