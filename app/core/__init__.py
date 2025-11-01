"""
Core module exports for easy importing.
"""
from app.core.config import settings
from app.core.database import (
    get_postgres_session,
    get_mongo_db,
    verify_connections,
    Base,
    engine,
)
from app.core.models import (
    Patient,
    HealthCondition,
    LifestyleFactor,
    HealthMetric,
    HealthcareAccess,
)
from app.core.mongo_models import (
    COLLECTIONS,
    Patient as MongoPatient,
    HealthCondition as MongoHealthCondition,
    LifestyleFactor as MongoLifestyleFactor,
    HealthMetric as MongoHealthMetric,
    HealthcareAccess as MongoHealthcareAccess,
)

__all__ = [
    "settings",
    "get_postgres_session",
    "get_mongo_db",
    "verify_connections",
    "Base",
    "engine",
    "Patient",
    "HealthCondition",
    "LifestyleFactor",
    "HealthMetric",
    "HealthcareAccess",
    "COLLECTIONS",
    "MongoPatient",
    "MongoHealthCondition",
    "MongoLifestyleFactor",
    "MongoHealthMetric",
    "MongoHealthcareAccess",
]