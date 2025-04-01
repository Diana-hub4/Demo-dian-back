# services/invoice_service.py
import uuid
from datetime import datetime
from models.invoice import Invoice, InvoiceItem, InvoiceSchema, InvoiceItemSchema
from services.dian_service import generate_cufe, generate_qr_code

class InvoiceService:
    
    @staticmethod
    def create_invoice(data):
        # Validar datos
        schema = InvoiceSchema()
        errors = schema.validate(data)
        if errors:
            raise ValueError(errors)
        
        # Generar CUFE y QR
        cufe = generate_cufe(data)
        qr_data = generate_qr_code(data)
        
        # Crear factura
        invoice_data = {
            **data,
            'cufe': cufe,
            'qr_code': qr_data,
            'issue_date': datetime.now()
        }
        
        invoice = Invoice(**invoice_data)
        invoice.save()
        
        # Crear items de factura si existen
        if 'items' in data:
            for item_data in data['items']:
                item_schema = InvoiceItemSchema()
                item_errors = item_schema.validate(item_data)
                if item_errors:
                    continue  # O manejar el error adecuadamente
                
                item = InvoiceItem(**{
                    **item_data,
                    'invoice_id': invoice.id
                })
                item.save()
        
        return invoice