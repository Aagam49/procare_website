import os
from pathlib import Path

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

from core.logger import logger

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'procare.db'}")

# Render / Heroku compatibility for postgres:// -> postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class LeadSubmission(Base):
    __tablename__ = "lead_submissions"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(200), nullable=False)
    preferred_date = Column(String(100), nullable=False)
    service = Column(String(200), nullable=False)
    symptoms = Column(Text, nullable=False)
    source = Column(String(50), default="homepage")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(30), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")
    except Exception as exc:
        logger.error(f"Failed to initialize database tables: {exc}", exc_info=True)
