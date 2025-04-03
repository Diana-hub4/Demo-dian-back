# src/models/__init__.py

# Exporta solo modelos y esquemas
from .clients import Client, ClientJsonSchema
from .taxes import Tax, TaxJsonSchema
from .paymentsTransfers import PaymentsTransfers, PaymentsTransfersJsonSchema
from .invoice import Invoice
from .generator import Generator
from .login import Login
from .dianVerification import DianVerification
from .model import Base
from .register import User, UserJsonSchema
from .pqrsf import PQRSF

# Lista todos los modelos y esquemas para exportar
__all__ = [
    'Client', 'ClientJsonSchema',
    'Tax', 'TaxJsonSchema',
    'PaymentsTransfers', 'PaymentsTransfersJsonSchema',
    'Invoice',
    'Generator',
    'Login',
    'DianVerification',
    'Base',
    'User', 'UserJsonSchema',
    'PQRSF'
]