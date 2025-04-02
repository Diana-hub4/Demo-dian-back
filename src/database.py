# src/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./HANA.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo necesario para SQLite
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SessionSql = SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from src.models.pqrsf import PQRSF  
    Base.metadata.create_all(bind=engine)
