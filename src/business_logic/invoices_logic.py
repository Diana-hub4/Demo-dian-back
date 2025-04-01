from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.invoice import InvoicesReceipts  # Importa el modelo InvoicesReceipts
from src.schemas.invoices_schema import InvoicesReceiptsJsonSchema  # Importa el esquema para serialización
from typing import Optional, Dict, Any

class InvoicesReceiptsLogic:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_invoice_receipt(self, invoice_data: Dict[str, Any]) -> InvoicesReceipts:
        """
        Crea un nuevo registro de factura o recibo.
        :param invoice_data: Diccionario con los datos de la factura o recibo.
        :return: Objeto InvoicesReceipts creado.
        :raises SQLAlchemyError: Si ocurre un error al guardar en la base de datos.
        """
        new_invoice = InvoicesReceipts(
            id_client=invoice_data["id_client"],
            electronic_invoice=invoice_data.get("electronic_invoice", "No"),  # Por defecto, "No"
            electronic_payroll=invoice_data.get("electronic_payroll", "No"),  # Por defecto, "No"
            support_document=invoice_data.get("support_document", "No"),  # Por defecto, "No"
            asset=invoice_data.get("asset", "No"),  # Por defecto, "No"
            liability=invoice_data.get("liability", "No"),  # Por defecto, "No"
            equity=invoice_data.get("equity", "No"),  # Por defecto, "No"
            non_supported_expenses=invoice_data.get("non_supported_expenses", "No"),  # Por defecto, "No"
            production_costs=invoice_data.get("production_costs", "No")  # Por defecto, "No"
        )

        try:
            self.db.add(new_invoice)
            self.db.commit()
            self.db.refresh(new_invoice)
            return new_invoice
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al crear la factura o recibo: {e}")

    def get_invoice_receipt(self, invoice_id: str) -> Optional[InvoicesReceipts]:
        """
        Obtiene una factura o recibo por su ID.
        :param invoice_id: ID de la factura o recibo.
        :return: Objeto InvoicesReceipts si existe, None si no se encuentra.
        """
        return self.db.query(InvoicesReceipts).filter(InvoicesReceipts.id == invoice_id).first()

    def update_invoice_receipt(self, invoice_id: str, update_data: Dict[str, Any]) -> Optional[InvoicesReceipts]:
        """
        Actualiza los datos de una factura o recibo existente.
        :param invoice_id: ID de la factura o recibo a actualizar.
        :param update_data: Diccionario con los datos a actualizar.
        :return: Objeto InvoicesReceipts actualizado.
        :raises ValueError: Si la factura o recibo no existe.
        :raises SQLAlchemyError: Si ocurre un error al actualizar.
        """
        invoice = self.get_invoice_receipt(invoice_id)
        if not invoice:
            raise ValueError("Factura o recibo no encontrado.")

        try:
            for key, value in update_data.items():
                if hasattr(invoice, key):
                    setattr(invoice, key, value)
            self.db.commit()
            self.db.refresh(invoice)
            return invoice
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al actualizar la factura o recibo: {e}")

    def delete_invoice_receipt(self, invoice_id: str) -> bool:
        """
        Elimina una factura o recibo por su ID.
        :param invoice_id: ID de la factura o recibo a eliminar.
        :return: True si se eliminó correctamente, False si no se encontró la factura o recibo.
        :raises SQLAlchemyError: Si ocurre un error al eliminar.
        """
        invoice = self.get_invoice_receipt(invoice_id)
        if not invoice:
            return False

        try:
            self.db.delete(invoice)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise SQLAlchemyError(f"Error al eliminar la factura o recibo: {e}")

    def calculate_income_expenses(self, client_id: str) -> Dict[str, float]:
        """
        Calcula los ingresos y egresos de un cliente basado en sus facturas y recibos.
        :param client_id: ID del cliente.
        :return: Diccionario con los totales de ingresos y egresos.
        """
        # Obtener todas las facturas y recibos del cliente
        invoices = self.db.query(InvoicesReceipts).filter(InvoicesReceipts.id_client == client_id).all()

        # Calcular ingresos y egresos
        income = 0.0
        expenses = 0.0

        for invoice in invoices:
            # Supongamos que los activos (assets) representan ingresos
            if invoice.asset == "Yes":
                income += 1.0  # Aquí deberías sumar el valor real de la factura
            # Supongamos que los pasivos (liability) representan egresos
            if invoice.liability == "Yes":
                expenses += 1.0  # Aquí deberías sumar el valor real de la factura

        return {
            "income": income,
            "expenses": expenses
        }

    def get_payment_methods(self, invoice_id: str) -> Dict[str, Any]:
        """
        Obtiene las formas de pago asociadas a una factura o recibo.
        :param invoice_id: ID de la factura o recibo.
        :return: Diccionario con las formas de pago.
        """
        # Simulación de formas de pago
        # En un entorno real, aquí se consultaría la base de datos o se integraría con un sistema de pagos
        payment_methods = {
            "cash": "Yes",  # Efectivo
            "credit_card": "No",  # Tarjeta de crédito
            "bank_transfer": "Yes"  # Transferencia bancaria
        }

        return payment_methods