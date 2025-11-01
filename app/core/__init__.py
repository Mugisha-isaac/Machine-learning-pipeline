"""
Core module exports for easy imports in API development.
"""
from app.core.database import (
    get_postgres_session,
    get_postgres_session_context,
    get_mongo_db,
    verify_connections,
    engine,
    SessionLocal,
    Base,
    mongo_db,
    mongo_client,
)
from app.core.config import settings
from app.core.models import (
    Patient,
    HealthCondition,
    LifestyleFactor,
    HealthMetric,
    HealthcareAccess,
)
from app.core.mongo_models import (
    Patient as MongoPatient,
    HealthCondition as MongoHealthCondition,
    LifestyleFactor as MongoLifestyleFactor,
    HealthMetric as MongoHealthMetric,
    HealthcareAccess as MongoHealthcareAccess,
    COLLECTIONS,
)

__all__ = [
    # Database
    "get_postgres_session",
    "get_postgres_session_context",
    "get_mongo_db",
    "verify_connections",
    "engine",
    "SessionLocal",
    "Base",
    "mongo_db",
    "mongo_client",
    # Config
    "settings",
    # PostgreSQL Models
    "Patient",
    "HealthCondition",
    "LifestyleFactor",
    "HealthMetric",
    "HealthcareAccess",
    # MongoDB Models
    "MongoPatient",
    "MongoHealthCondition",
    "MongoLifestyleFactor",
    "MongoHealthMetric",
    "MongoHealthcareAccess",
    "COLLECTIONS",
]

