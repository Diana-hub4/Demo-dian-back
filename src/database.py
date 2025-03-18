from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

# Configuración de DB (ajusta tu string de conexión)
DATABASE_URL = "sqlite:///./HANA.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionSql = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionSql()
    try:
        yield db
    finally:
        db.close()
