from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.generator import Generator  # Importa el modelo Generator
from src.schemas.generator_schema import GeneratorJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any

class GeneratorLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_generator(self, generator_data: Dict[str, Any]) -> Generator:
        """
        Crea un nuevo registro de generación de factura electrónica o documento soporte.
        :param generator_data: Diccionario con los datos del generador.
        :return: Objeto Generator creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_generator = Generator(
            id_payment_transfer=generator_data["id_payment_transfer"],
            electronic_invoice=generator_data.get("electronic_invoice", "No"),  # Por defecto, "No"
            cufe=generator_data.get("cufe", ""),  # Por defecto, vacío
            qr_code=generator_data.get("qr_code", ""),  # Por defecto, vacío
            invoice_pdf=generator_data.get("invoice_pdf", b"")  # Por defecto, bytes vacíos
        )

        try:
            self.db.add(new_generator)
            self.db.commit()
            self.db.refresh(new_generator)
            return new_generator
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear el generador: {e}")

    def get_generator(self, generator_id: str) -> Optional[Generator]:
        """
        Obtiene un generador por su ID.
        :param generator_id: ID del generador.
        :return: Objeto Generator si existe, None si no se encuentra.
        """
        return self.db.query(Generator).filter(Generator.id == generator_id).first()

    def update_generator(self, generator_id: str, update_data: Dict[str, Any]) -> Optional[Generator]:
        """
        Actualiza los datos de un generador existente.
        :param generator_id: ID del generador a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto Generator actualizado.
        :raises ValueError: Si el generador no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        generator = self.get_generator(generator_id)
        if not generator:
            raise ValueError("Generador no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(generator, key):
                    setattr(generator, key, value)
            self.db.commit()
            self.db.refresh(generator)
            return generator
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar el generador: {e}")

    def delete_generator(self, generator_id: str) -> bool:
        """
        Elimina un generador por su ID.
        :param generator_id: ID del generador a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el generador.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        generator = self.get_generator(generator_id)
        if not generator:
            return False

        try:
            self.db.delete(generator)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar el generador: {e}")

    def generate_electronic_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera una factura electrónica con los datos proporcionados.
        :param invoice_data: Diccionario con los datos de la factura.
        :return: Respuesta con los datos generados (CUFE, QR, PDF, etc.).
        """
        # Simulación de generación de factura electrónica
        # En un entorno real, aquí se haría la generación del CUFE, QR y PDF
        generated_data = {
            "cufe": "CUFE_GENERADO_123456789",  # Simulación de CUFE
            "qr_code": "QR_CODE_GENERADO_123456789",  # Simulación de código QR
            "invoice_pdf": b"PDF_GENERADO"  # Simulación de PDF (en bytes)
        }

        # Guardar los datos generados en la base de datos
        generator_data = {
            "id_payment_transfer": invoice_data.get("id_payment_transfer"),
            "electronic_invoice": "Yes",  # Indicar que es una factura electrónica
            "cufe": generated_data["cufe"],
            "qr_code": generated_data["qr_code"],
            "invoice_pdf": generated_data["invoice_pdf"]
        }
        self.create_generator(generator_data)

        return generated_data