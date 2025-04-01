# services/dian_service.py
import hashlib
import io
import json
from datetime import datetime
import uuid
import qrcode # type: ignore
import base64

def generate_cufe(invoice_data):
    """
    Genera el Código Único de Factura Electrónica (CUFE) según especificaciones DIAN
    """
    # Datos requeridos para el CUFE
    required_data = {
        'invoice_number': invoice_data['invoice_number'],
        'issue_date': datetime.now().strftime('%Y-%m-%d'),
        'total': str(invoice_data['total']),
        'client_id': invoice_data['client_id'],
        'company_nit': '123456789-1',  # Reemplazar con NIT real de la empresa
        'technical_key': 'clave-tecnica'  # Reemplazar con clave técnica real
    }
    
    # Convertir a JSON y luego a hash SHA-384
    json_data = json.dumps(required_data, sort_keys=True)
    hash_object = hashlib.sha384(json_data.encode())
    cufe = hash_object.hexdigest().upper()
    
    return cufe

def generate_qr_code(invoice_data):
    """
    Genera el código QR con los datos de la factura según requerimientos DIAN
    """
    qr_data = {
        'id': str(uuid.uuid4()),
        'invoice_number': invoice_data['invoice_number'],
        'issue_date': datetime.now().isoformat(),
        'total': invoice_data['total'],
        'total_taxes': invoice_data.get('total_taxes', 0),
        'cufe': generate_cufe(invoice_data),
        'company_nit': '123456789-1',  # Reemplazar con NIT real
        'company_name': 'Nombre de la Empresa'  # Reemplazar con nombre real
    }
    
    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a base64 para almacenamiento
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return qr_base64
