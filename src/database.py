## src\database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from src.models import login, register  # importa tus modelos aquí
    from src.models.nomina import Nomina  # importa tus modelos aquí
    from src.models.pqrsf import PQRSF  # importa tus modelos aqui
    from src.models.register import User  # importa tus modelos aquí
    from src.models.suppliers import Supplier  # importa tus modelos aquí
    from src.models.taxes import Taxes  # importa tus modelos aquí
    from src.models.paymentsTransfers import PaymentsTransfers  # importa tus modelos aquí
    from src.models.invoice import Invoice  # importa tus modelos aquí
    from src.models.generator import Generator  # importa tus modelos aquí
    from src.models.dianVerification import DianVerification  # importa tus modelos aquí
    from src.models.clients import Client  # importa tus modelos aquí
    from src.models.forgot_password import PasswordResetToken  # importa tus modelos aquí
    from src.models.generator import  Generator # importa tus modelos aquí

    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()