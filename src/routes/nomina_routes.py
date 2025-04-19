# src/routes/nomina_routes.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import os
from typing import List
from ..models.nomina import Nomina, create_nomina
from ..schemas.nomina_schema import NominaRequest, NominaResponse
from ..database import SessionLocal

router = APIRouter(prefix="/nominas", tags=["Nóminas"])

# Configuración
PDF_STORAGE = "storage/nominas"
os.makedirs(PDF_STORAGE, exist_ok=True)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una nueva nómina
@router.post("/nomina", response_model=NominaResponse)
async def create_new_nomina(nomina: NominaRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Crear una nueva nómina
        new_nomina = create_nomina(
            id_user=nomina.id_user,
            contract_type=nomina.contract_type.value,
            period=nomina.period,
            employee_name=nomina.employee_name,
            salary=nomina.salary,
            deductions=nomina.deductions,
            email=nomina.email,
            contributions=nomina.contributions
        )
        db.add(new_nomina)
        db.commit()
        db.refresh(new_nomina)
        return new_nomina
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener una nómina por ID
@router.post("/", response_model=NominaResponse)
async def create_nomina(
    nomina_data: Union[NominaRequest, NominaCreate],
    db: Session = Depends(get_db)
):
    try:
        # Cálculos de ley colombiana
        health = nomina_data.base_salary * 0.04
        pension = nomina_data.base_salary * 0.04
        solidarity = 0
        
        if nomina_data.base_salary > 4 * 1160000:  # 4 SMLV 2023
            solidarity = nomina_data.base_salary * 0.01
        
        # Cálculo de horas extras
        extra_payments = (
            (nomina_data.extra_day_hours * (nomina_data.base_salary / 240) * 1.25) +
            (nomina_data.extra_night_hours * (nomina_data.base_salary / 240) * 1.75) +
            (nomina_data.sunday_hours * (nomina_data.base_salary / 240) * 1.75) +
            (nomina_data.holiday_hours * (nomina_data.base_salary / 240) * 2.0)
        )
        
        total_gross = (
            nomina_data.base_salary * (nomina_data.days_worked / 30) +
            nomina_data.transport_allowance +
            extra_payments
        )
        
        total_deductions = (
            health + pension + solidarity + 
            nomina_data.deductions
        )
        
        total_net = total_gross - total_deductions
        
        # Crear registro en BD
        nomina = Nomina(
            id_user=nomina_data.id_user,
            contract_type=nomina_data.contract_type.value,
            period=nomina_data.period,
            employee_id=nomina_data.employee_id,
            employee_name=nomina_data.employee_name,
            base_salary=nomina_data.base_salary,
            transport_allowance=nomina_data.transport_allowance,
            days_worked=nomina_data.days_worked,
            night_hours=nomina_data.night_hours,
            extra_day_hours=nomina_data.extra_day_hours,
            extra_night_hours=nomina_data.extra_night_hours,
            sunday_hours=nomina_data.sunday_hours,
            holiday_hours=nomina_data.holiday_hours,
            health_contribution=health,
            pension_contribution=pension,
            solidarity_pension_fund=solidarity,
            deductions=nomina_data.deductions,
            other_concepts=nomina_data.other_concepts,
            total_gross=total_gross,
            total_net=total_net
        )
        
        db.add(nomina)
        db.commit()
        db.refresh(nomina)
        
        # Generar PDF
        pdf_path = f"{PDF_STORAGE}/nomina_{nomina.id}.pdf"
        generate_pdf(nomina, pdf_path)
        
        # Actualizar con URL del PDF
        nomina.pdf_url = pdf_path
        db.commit()
        
        return nomina
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def generate_pdf(nomina: Nomina, output_path: str):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"NÓMINA DE PAGO - {nomina.period}")
    
    # Información empleado
    c.setFont("Helvetica", 12)
    y = 700
    c.drawString(100, y, f"Empleado: {nomina.employee_name} ({nomina.employee_id})")
    y -= 20
    c.drawString(100, y, f"Tipo Contrato: {nomina.contract_type}")
    y -= 20
    c.drawString(100, y, f"Días trabajados: {nomina.days_worked}")
    
    # Detalles de pago
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "DESGLOSE DE PAGOS")
    y -= 30
    
    # Tabla de conceptos
    concepts = [
        ("Salario básico", nomina.base_salary),
        ("Auxilio transporte", nomina.transport_allowance),
        ("Horas extras diurnas", (nomina.extra_day_hours * (nomina.base_salary / 240) * 1.25)),
        ("Horas extras nocturnas", (nomina.extra_night_hours * (nomina.base_salary / 240) * 1.75)),
        ("Horas dominicales/festivas", ((nomina.sunday_hours + nomina.holiday_hours) * (nomina.base_salary / 240) * 1.75)),
        ("Total Devengado", nomina.total_gross),
        ("", ""),
        ("Aportes Salud", nomina.health_contribution),
        ("Aportes Pensión", nomina.pension_contribution),
        ("Fondo Solidaridad Pensional", nomina.solidarity_pension_fund),
        ("Otros descuentos", nomina.deductions),
        ("Total Deducciones", (nomina.health_contribution + nomina.pension_contribution + nomina.solidarity_pension_fund + nomina.deductions)),
        ("", ""),
        ("NETO A PAGAR", nomina.total_net)
    ]
    
    c.setFont("Helvetica", 12)
    for concept, value in concepts:
        c.drawString(100, y, concept)
        c.drawString(400, y, f"${value:,.2f}" if value != "" else "")
        y -= 20
    
    # Pie de página
    y -= 30
    c.drawString(100, y, "Firma empleador: __________________________")
    y -= 20
    c.drawString(100, y, "Firma empleado: __________________________")
    
    c.save()
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())

# Endpoint para eliminar una nómina
@router.delete("/nomina/{nomina_id}")
async def delete_nomina(nomina_id: str, db: SessionLocal = Depends(get_db)):
    try:
        nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
        if not nomina:
            raise HTTPException(status_code=404, detail="Nómina no encontrada")

        db.delete(nomina)
        db.commit()
        return {"message": "Nómina eliminada correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{nomina_id}/pdf", response_class=FileResponse)
async def download_nomina_pdf(nomina_id: str, db: Session = Depends(get_db)):
    nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
    if not nomina or not nomina.pdf_url:
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    
    return FileResponse(
        nomina.pdf_url,
        filename=f"nomina_{nomina.employee_id}_{nomina.period}.pdf"
    )

@router.get("/empleado/{employee_id}", response_model=List[NominaResponse])
async def get_employee_nominas(employee_id: str, db: Session = Depends(get_db)):
    return db.query(Nomina).filter(Nomina.employee_id == employee_id).all()

@router.post("/{nomina_id}/pagar")
async def mark_as_paid(nomina_id: str, db: Session = Depends(get_db)):
    nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
    if not nomina:
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    
    nomina.is_paid = True
    nomina.payment_date = datetime.now()
    db.commit()
    
    return {"message": "Nómina marcada como pagada"}