from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.pqrsf import PQRSF  # Importa el modelo PQRSF
from src.schemas.pqrsf_schema import PQRSFJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any, List

class PQRSFLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_pqrsf(self, pqrsf_data: Dict[str, Any]) -> PQRSF:
        """
        Crea una nueva solicitud PQRSF.
        :param pqrsf_data: Diccionario con los datos de la solicitud PQRSF.
        :return: Objeto PQRSF creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_pqrsf = PQRSF(
            pqrsf_type=pqrsf_data["pqrsf_type"],
            message=pqrsf_data["message"]
        )

        try:
            self.db.add(new_pqrsf)
            self.db.commit()
            self.db.refresh(new_pqrsf)
            return new_pqrsf
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear la solicitud PQRSF: {e}")

    def get_pqrsf(self, pqrsf_id: str) -> Optional[PQRSF]:
        """
        Obtiene una solicitud PQRSF por su ID.
        :param pqrsf_id: ID de la solicitud PQRSF.
        :return: Objeto PQRSF si existe, None si no se encuentra.
        """
        return self.db.query(PQRSF).filter(PQRSF.id == pqrsf_id).first()

    def update_pqrsf(self, pqrsf_id: str, update_data: Dict[str, Any]) -> Optional[PQRSF]:
        """
        Actualiza los datos de una solicitud PQRSF existente.
        :param pqrsf_id: ID de la solicitud PQRSF a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto PQRSF actualizado.
        :raises ValueError: Si la solicitud PQRSF no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        pqrsf = self.get_pqrsf(pqrsf_id)
        if not pqrsf:
            raise ValueError("Solicitud PQRSF no encontrada.")

        try:
            for key, value in update_data.items():
                if hasattr(pqrsf, key):
                    setattr(pqrsf, key, value)
            self.db.commit()
            self.db.refresh(pqrsf)
            return pqrsf
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar la solicitud PQRSF: {e}")

    def delete_pqrsf(self, pqrsf_id: str) -> bool:
        """
        Elimina una solicitud PQRSF por su ID.
        :param pqrsf_id: ID de la solicitud PQRSF a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró la solicitud PQRSF.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        pqrsf = self.get_pqrsf(pqrsf_id)
        if not pqrsf:
            return False

        try:
            self.db.delete(pqrsf)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar la solicitud PQRSF: {e}")

    def get_all_pqrsf(self) -> List[PQRSF]:
        """
        Obtiene todas las solicitudes PQRSF.
        :return: Lista de objetos PQRSF.
        """
        return self.db.query(PQRSF).all()

    def process_pqrsf(self, pqrsf_id: str) -> Dict[str, Any]:
        """
        Procesa una solicitud PQRSF (simulación).
        :param pqrsf_id: ID de la solicitud PQRSF a procesar.
        :return: Diccionario con el resultado del procesamiento.
        """
        pqrsf = self.get_pqrsf(pqrsf_id)
        if not pqrsf:
            raise ValueError("Solicitud PQRSF no encontrada.")

        # Simulación de procesamiento
        processing_result = {
            "status": "processed",
            "message": f"La solicitud PQRSF de tipo {pqrsf.pqrsf_type} ha sido procesada."
        }

        return processing_result