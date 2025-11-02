"""
Database connection and session management for PostgreSQL and MongoDB.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from pymongo import MongoClient
from pymongo.database import Database
from typing import Generator
from contextlib import contextmanager

from app.core.config import settings


# Base class for SQLAlchemy models (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass


# PostgreSQL setup
def get_postgres_url() -> str:
    """Get PostgreSQL connection URL."""
    if settings.POSTGRES_URL:
        return settings.POSTGRES_URL
    
    # Build URL from components
    if all([settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_HOST, settings.POSTGRES_DB]):
        port = f":{settings.POSTGRES_PORT}" if settings.POSTGRES_PORT else ":5432"
        return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}{port}/{settings.POSTGRES_DB}"
    
    raise ValueError("PostgreSQL connection URL or components must be provided in .env file")


SQLALCHEMY_DATABASE_URL = get_postgres_url()

# Create engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    echo=False,  # Set to True for SQL query logging
    pool_size=5,
    max_overflow=10,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# Dependency for FastAPI
def get_postgres_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for PostgreSQL database sessions.
    Usage: 
        @app.get("/items")
        def read_items(db: Session = Depends(get_postgres_session)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_postgres_session_context():
    """
    Context manager for PostgreSQL sessions (for use outside FastAPI).
    Usage:
        with get_postgres_session_context() as db:
            db.query(Patient).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# MongoDB setup
mongo_client: MongoClient = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000,  # Timeout for connection
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
)

# Get MongoDB database
mongo_db: Database = mongo_client[settings.MONGO_DB]


def get_mongo_db() -> Database:
    """
    Get MongoDB database instance.
    Usage in FastAPI:
        db = get_mongo_db()
        collection = db["ml_models"]
    """
    return mongo_db


def verify_connections():
    """Verify both database connections are working."""
    # Test PostgreSQL connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("PostgreSQL connection successful")
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        raise
    
    # Test MongoDB connection
    try:
        mongo_client.server_info()
        print("MongoDB connection successful")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        raise
