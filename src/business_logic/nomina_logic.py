from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.nomina import Nomina  # Importa el modelo Nomina
from src.schemas.nomina_schema import NominaJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any, List

class NominaLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_nomina(self, nomina_data: Dict[str, Any]) -> Nomina:
        """
        Crea una nueva nómina en la base de datos.
        :param nomina_data: Diccionario con los datos de la nómina.
        :return: Objeto Nomina creado.
        :raises ValueError: Si ya existe una nómina para el mismo empleado en el mismo período.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        # Verifica si ya existe una nómina para el mismo empleado en el mismo período
        existing_nomina = self.db.query(Nomina).filter(
            (Nomina.employee_name == nomina_data["employee_name"]) &
            (Nomina.period == nomina_data["period"])
        ).first()
        if existing_nomina:
            raise ValueError("Ya existe una nómina para este empleado en el período especificado.")

        # Crea una nueva nómina
        new_nomina = Nomina(
            id_user=nomina_data["id_user"],
            contract_type=nomina_data["contract_type"],
            period=nomina_data["period"],
            employee_name=nomina_data["employee_name"],
            salary=nomina_data["salary"],
            deductions=nomina_data.get("deductions", 0.0),  # Por defecto, 0.0
            email=nomina_data["email"],
            contributions=nomina_data["contributions"]
        )

        try:
            self.db.add(new_nomina)
            self.db.commit()
            self.db.refresh(new_nomina)
            return new_nomina
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear la nómina: {e}")

    def get_nomina(self, nomina_id: str) -> Optional[Nomina]:
        """
        Obtiene una nómina por su ID.
        :param nomina_id: ID de la nómina.
        :return: Objeto Nomina si existe, None si no se encuentra.
        """
        return self.db.query(Nomina).filter(Nomina.id == nomina_id).first()

    def update_nomina(self, nomina_id: str, update_data: Dict[str, Any]) -> Optional[Nomina]:
        """
        Actualiza los datos de una nómina existente.
        :param nomina_id: ID de la nómina a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto Nomina actualizado.
        :raises ValueError: Si la nómina no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        nomina = self.get_nomina(nomina_id)
        if not nomina:
            raise ValueError("Nómina no encontrada.")

        try:
            for key, value in update_data.items():
                if hasattr(nomina, key):
                    setattr(nomina, key, value)
            self.db.commit()
            self.db.refresh(nomina)
            return nomina
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar la nómina: {e}")

    def delete_nomina(self, nomina_id: str) -> bool:
        """
        Elimina una nómina por su ID.
        :param nomina_id: ID de la nómina a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró la nómina.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        nomina = self.get_nomina(nomina_id)
        if not nomina:
            return False

        try:
            self.db.delete(nomina)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar la nómina: {e}")

    def get_nominas_by_employee(self, employee_name: str) -> List[Nomina]:
        """
        Obtiene todas las nóminas de un empleado.
        :param employee_name: Nombre del empleado.
        :return: Lista de objetos Nomina.
        """
        return self.db.query(Nomina).filter(Nomina.employee_name == employee_name).all()

    def get_nominas_last_12_months(self) -> List[Nomina]:
        """
        Obtiene todas las nóminas de los últimos 12 meses.
        :return: Lista de objetos Nomina.
        """
        # Calcula la fecha de hace 12 meses
        twelve_months_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m")

        # Obtiene las nóminas de los últimos 12 meses
        return self.db.query(Nomina).filter(Nomina.period >= twelve_months_ago).all()