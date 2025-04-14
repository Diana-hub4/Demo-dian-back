# src/models/__init__.py

from .clients import Client, ClientJsonSchema
from .taxes import Tax, TaxJsonSchema
from .paymentsTransfers import PaymentsTransfers, PaymentsTransfersJsonSchema
from .invoice import Invoice
from .generator import Generator
from .login import Login
from .dianVerification import DianVerification
from .model import Base
from .register import User
from .pqrsf import PQRSF
from src.schemas.register_schema import UserJsonSchema
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .login import Login
    from .register import User

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
