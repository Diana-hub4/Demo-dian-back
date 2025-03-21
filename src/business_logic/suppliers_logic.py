from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.suppliers import Supplier  # Importa el modelo Supplier
from src.schemas.suppliers_schema import SupplierJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any, List

class SuppliersLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_supplier(self, supplier_data: Dict[str, Any]) -> Supplier:
        """
        Crea un nuevo proveedor en la base de datos.
        :param supplier_data: Diccionario con los datos del proveedor.
        :return: Objeto Supplier creado.
        :raises ValueError: Si el proveedor ya está registrado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        # Verifica si el proveedor ya existe (por NIT o correo electrónico)
        existing_supplier = self.db.query(Supplier).filter(
            (Supplier.tax_id == supplier_data["tax_id"]) | (Supplier.email == supplier_data["email"])
        ).first()
        if existing_supplier:
            raise ValueError("El proveedor ya está registrado.")

        # Crea un nuevo proveedor
        new_supplier = Supplier(
            id_user=supplier_data["id_user"],
            name=supplier_data["name"],
            person_type=supplier_data["person_type"],
            tax_id=supplier_data["tax_id"],
            document_type=supplier_data["document_type"],
            identification_number=supplier_data["identification_number"],
            business_reason=supplier_data["business_reason"],
            email=supplier_data["email"],
            contact_number=supplier_data["contact_number"],
            address=supplier_data["address"],
            city=supplier_data["city"],
            regime_type=supplier_data["regime_type"],
            status=supplier_data.get("status", "active")  # Por defecto, "active"
        )

        try:
            self.db.add(new_supplier)
            self.db.commit()
            self.db.refresh(new_supplier)
            return new_supplier
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear el proveedor: {e}")

    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        """
        Obtiene un proveedor por su ID.
        :param supplier_id: ID del proveedor.
        :return: Objeto Supplier si existe, None si no se encuentra.
        """
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def update_supplier(self, supplier_id: str, update_data: Dict[str, Any]) -> Optional[Supplier]:
        """
        Actualiza los datos de un proveedor existente.
        :param supplier_id: ID del proveedor a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto Supplier actualizado.
        :raises ValueError: Si el proveedor no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        supplier = self.get_supplier(supplier_id)
        if not supplier:
            raise ValueError("Proveedor no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(supplier, key):
                    setattr(supplier, key, value)
            self.db.commit()
            self.db.refresh(supplier)
            return supplier
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar el proveedor: {e}")

    def delete_supplier(self, supplier_id: str) -> bool:
        """
        Elimina un proveedor por su ID.
        :param supplier_id: ID del proveedor a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el proveedor.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        supplier = self.get_supplier(supplier_id)
        if not supplier:
            return False

        try:
            self.db.delete(supplier)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar el proveedor: {e}")

    def get_all_suppliers(self) -> List[Supplier]:
        """
        Obtiene todos los proveedores registrados.
        :return: Lista de objetos Supplier.
        """
        return self.db.query(Supplier).all()

    def get_suppliers_by_user(self, user_id: str) -> List[Supplier]:
        """
        Obtiene todos los proveedores asociados a un usuario (contador).
        :param user_id: ID del usuario (contador).
        :return: Lista de objetos Supplier.
        """
        return self.db.query(Supplier).filter(Supplier.id_user == user_id).all()