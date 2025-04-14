from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.models.nomina import Nomina  
from src.schemas.nomina_schema import NominaSchema  
from typing import Optional, Dict, Any, List

class NominaLogic:
    # Constantes para cálculos
    EXTRA_HOUR_RATE = 1.25  # Multiplicador por hora extra
    LATE_PENALTY_RATE = 0.01  # Penalización por minuto tarde
    DEFAULT_WORK_HOURS_MONTH = 160  # Horas laborales por mes (para cálculos)

    def __init__(self, db_session: Session):
        self.db = db_session

    def _calculate_payroll_values(self, nomina_data: Dict[str, Any]) -> Dict[str, float]:
        """Calcula los valores derivados de la nómina."""
        salario_base = nomina_data["salario_base"]
        horas_extras = nomina_data.get("horas_extras", 0.0)
        retrasos = nomina_data.get("retrasos", 0.0)
        transporte = nomina_data.get("transporte", 0.0)
        vacaciones = nomina_data.get("vacaciones", 0.0)
        deductions = nomina_data.get("deductions", 0.0)
        contributions = nomina_data.get("contributions", 0.0)

        # Cálculo de valores
        extra_pay = (salario_base / self.DEFAULT_WORK_HOURS_MONTH) * self.EXTRA_HOUR_RATE * horas_extras
        late_penalty = (salario_base / self.DEFAULT_WORK_HOURS_MONTH / 60) * self.LATE_PENALTY_RATE * retrasos

        total_ingresos = salario_base + extra_pay + transporte + vacaciones
        total_deducciones = late_penalty + deductions
        total_neto = total_ingresos - total_deducciones + contributions

        return {
            "horas_extras": horas_extras,
            "extra_pay": extra_pay,
            "retrasos": retrasos,
            "late_penalty": late_penalty,
            "transporte": transporte,
            "vacaciones": vacaciones,
            "total_ingresos": total_ingresos,
            "total_deducciones": total_deducciones,
            "total_neto": total_neto
        }

    def create_nomina(self, nomina_data: Dict[str, Any]) -> Nomina:
        """
        Crea una nueva nómina en la base de datos.
        
        Args:
            nomina_data: Diccionario con los datos de la nómina.
                Campos requeridos: id_user, contract_type, period, employee_name, 
                employee_id, email, salario_base, days_worked, 
                health_contribution, pension_contribution
            
        Returns:
            Objeto Nomina creado
            
        Raises:
            ValueError: Si ya existe una nómina para el mismo empleado en el mismo período
            SQLAlchemyError: Si ocurre un error al guardar en la base de datos
        """
        # Verifica si ya existe una nómina para el mismo empleado en el mismo período
        existing_nomina = self.db.query(Nomina).filter(
            (Nomina.employee_id == nomina_data["employee_id"]) & 
            (Nomina.period == nomina_data["period"])
        ).first()
        
        if existing_nomina:
            raise ValueError("Ya existe una nómina para este empleado en el período especificado.")

        # Calcula valores derivados
        calculated_values = self._calculate_payroll_values(nomina_data)

        # Crea una nueva nómina
        new_nomina = Nomina(
            id_user=nomina_data["id_user"],
            contract_type=nomina_data["contract_type"],
            period=nomina_data["period"],
            employee_name=nomina_data["employee_name"],
            employee_id=nomina_data["employee_id"],
            email=nomina_data["email"],
            cargo=nomina_data.get("cargo"),
            
            # Salarios e ingresos
            salario_base=nomina_data["salario_base"],
            horas_extras=calculated_values["horas_extras"],
            transporte=calculated_values["transporte"],
            vacaciones=calculated_values["vacaciones"],
            total_ingresos=calculated_values["total_ingresos"],
            
            # Tiempo trabajado
            days_worked=nomina_data["days_worked"],
            night_hours=nomina_data.get("night_hours", 0.0),
            extra_day_hours=nomina_data.get("extra_day_hours", 0.0),
            extra_night_hours=nomina_data.get("extra_night_hours", 0.0),
            sunday_hours=nomina_data.get("sunday_hours", 0.0),
            holiday_hours=nomina_data.get("holiday_hours", 0.0),
            retrasos=calculated_values["retrasos"],
            
            # Deducciones y aportes
            health_contribution=nomina_data["health_contribution"],
            pension_contribution=nomina_data["pension_contribution"],
            solidarity_pension_fund=nomina_data.get("solidarity_pension_fund", 0.0),
            deductions=nomina_data.get("deductions", 0.0),
            total_deducciones=calculated_values["total_deducciones"],
            
            # Totales
            total_neto=calculated_values["total_neto"],
            
            # Otros campos
            other_concepts=nomina_data.get("other_concepts"),
            is_paid=nomina_data.get("is_paid", False),
            payment_date=nomina_data.get("payment_date"),
            pdf_url=nomina_data.get("pdf_url")
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
        """Obtiene una nómina por su ID."""
        return self.db.query(Nomina).filter(Nomina.id == nomina_id).first()

    def update_nomina(self, nomina_id: str, update_data: Dict[str, Any]) -> Optional[Nomina]:
        """
        Actualiza los datos de una nómina existente.
        
        Args:
            nomina_id: ID de la nómina a actualizar
            update_data: Diccionario con los datos a actualizar
            
        Returns:
            Objeto Nomina actualizado
            
        Raises:
            ValueError: Si la nómina no existe
            SQLAlchemyError: Si ocurre un error al actualizar
        """
        nomina = self.get_nomina(nomina_id)
        if not nomina:
            raise ValueError("Nómina no encontrada.")

        # Si se actualizan campos de cálculo, recalcular valores
        if any(field in update_data for field in [
            'salario_base', 'horas_extras', 'retrasos', 
            'transporte', 'vacaciones', 'deductions', 'contributions'
        ]):
            # Combinar datos existentes con los nuevos
            nomina_data = {**nomina.__dict__, **update_data}
            calculated_values = self._calculate_payroll_values(nomina_data)
            update_data.update({
                'total_ingresos': calculated_values['total_ingresos'],
                'total_deducciones': calculated_values['total_deducciones'],
                'total_neto': calculated_values['total_neto']
            })

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
        """Elimina una nómina por su ID."""
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

    def get_nominas_by_employee(self, employee_id: str) -> List[Nomina]:
        """Obtiene todas las nóminas de un empleado por su ID."""
        return self.db.query(Nomina).filter(Nomina.employee_id == employee_id).all()

    def get_nominas_last_12_months(self) -> List[Nomina]:
        """Obtiene todas las nóminas de los últimos 12 meses."""
        twelve_months_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m")
        return self.db.query(Nomina).filter(Nomina.period >= twelve_months_ago).all()