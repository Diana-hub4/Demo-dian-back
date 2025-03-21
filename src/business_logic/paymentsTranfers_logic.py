from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.paymentsTransfers import PaymentsTransfers  # Importa el modelo PaymentsTransfers
from src.schemas.paymentsTransfers_schema import PaymentsTransfersJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any, List

class PaymentsTransfersLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_payment_transfer(self, payment_data: Dict[str, Any]) -> PaymentsTransfers:
        """
        Crea un nuevo registro de pago o transferencia.
        :param payment_data: Diccionario con los datos del pago o transferencia.
        :return: Objeto PaymentsTransfers creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_payment = PaymentsTransfers(
            id_tax=payment_data["id_tax"],
            bank_transfer=payment_data.get("bank_transfer", "No"),  # Por defecto, "No"
            cash_payment=payment_data.get("cash_payment", "No"),  # Por defecto, "No"
            credit_card_payment=payment_data.get("credit_card_payment", "No"),  # Por defecto, "No"
            debit_card_payment=payment_data.get("debit_card_payment", "No"),  # Por defecto, "No"
            barter=payment_data.get("barter", "No")  # Por defecto, "No"
        )

        try:
            self.db.add(new_payment)
            self.db.commit()
            self.db.refresh(new_payment)
            return new_payment
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear el pago o transferencia: {e}")

    def get_payment_transfer(self, payment_id: str) -> Optional[PaymentsTransfers]:
        """
        Obtiene un pago o transferencia por su ID.
        :param payment_id: ID del pago o transferencia.
        :return: Objeto PaymentsTransfers si existe, None si no se encuentra.
        """
        return self.db.query(PaymentsTransfers).filter(PaymentsTransfers.id == payment_id).first()

    def update_payment_transfer(self, payment_id: str, update_data: Dict[str, Any]) -> Optional[PaymentsTransfers]:
        """
        Actualiza los datos de un pago o transferencia existente.
        :param payment_id: ID del pago o transferencia a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto PaymentsTransfers actualizado.
        :raises ValueError: Si el pago o transferencia no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        payment = self.get_payment_transfer(payment_id)
        if not payment:
            raise ValueError("Pago o transferencia no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(payment, key):
                    setattr(payment, key, value)
            self.db.commit()
            self.db.refresh(payment)
            return payment
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar el pago o transferencia: {e}")

    def delete_payment_transfer(self, payment_id: str) -> bool:
        """
        Elimina un pago o transferencia por su ID.
        :param payment_id: ID del pago o transferencia a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró el pago o transferencia.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        payment = self.get_payment_transfer(payment_id)
        if not payment:
            return False

        try:
            self.db.delete(payment)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar el pago o transferencia: {e}")

    def get_payments_by_tax(self, tax_id: str) -> List[PaymentsTransfers]:
        """
        Obtiene todos los pagos o transferencias asociados a un impuesto.
        :param tax_id: ID del impuesto.
        :return: Lista de objetos PaymentsTransfers.
        """
        return self.db.query(PaymentsTransfers).filter(PaymentsTransfers.id_tax == tax_id).all()

    def calculate_total_payments(self, tax_id: str) -> Dict[str, float]:
        """
        Calcula el total de dinero ingresado por cada forma de pago para un impuesto específico.
        :param tax_id: ID del impuesto.
        :return: Diccionario con los totales de dinero por forma de pago.
        """
        payments = self.get_payments_by_tax(tax_id)

        # Inicializar totales
        totals = {
            "bank_transfer": 0.0,
            "cash_payment": 0.0,
            "credit_card_payment": 0.0,
            "debit_card_payment": 0.0,
            "barter": 0.0
        }

        # Sumar los montos de cada forma de pago
        for payment in payments:
            if payment.bank_transfer == "Yes":
                totals["bank_transfer"] += 1.0  # Aquí deberías sumar el valor real del pago
            if payment.cash_payment == "Yes":
                totals["cash_payment"] += 1.0  # Aquí deberías sumar el valor real del pago
            if payment.credit_card_payment == "Yes":
                totals["credit_card_payment"] += 1.0  # Aquí deberías sumar el valor real del pago
            if payment.debit_card_payment == "Yes":
                totals["debit_card_payment"] += 1.0  # Aquí deberías sumar el valor real del pago
            if payment.barter == "Yes":
                totals["barter"] += 1.0  # Aquí deberías sumar el valor real del pago

        return totals