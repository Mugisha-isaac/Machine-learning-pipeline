"""
Pytest configuration and fixtures for testing.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from bson import ObjectId

from app.main import app
from app.core.database import Base, get_postgres_session, get_mongo_db
from app.core.config import settings

# Test database URLs
TEST_POSTGRES_URL = "sqlite:///./test.db"  # Use SQLite for testing
TEST_MONGO_DB = "test_healthcare_ml"


# PostgreSQL Test Setup
@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    engine = create_engine(TEST_POSTGRES_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_postgres_session] = override_get_db
    
    yield TestingSessionLocal()
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


# MongoDB Test Setup
@pytest.fixture(scope="function")
def test_mongo_db():
    """Create a test MongoDB database."""
    client = MongoClient(settings.MONGO_URI)
    db = client[TEST_MONGO_DB]
    
    def override_get_mongo_db():
        return db
    
    app.dependency_overrides[get_mongo_db] = override_get_mongo_db
    
    yield db
    
    # Cleanup - drop all collections
    for collection_name in db.list_collection_names():
        db[collection_name].drop()
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing."""
    return {
        "Sex": True,
        "Age": 45,
        "Education": 4,
        "Income": 75000
    }


@pytest.fixture
def sample_health_condition_data():
    """Sample health condition data for testing."""
    return {
        "PatientID": 1,
        "Diabetes_012": False,
        "HighBP": True,
        "HighChol": True,
        "Stroke": False,
        "HeartDiseaseorAttack": False,
        "DiffWalk": False
    }


@pytest.fixture
def sample_lifestyle_factor_data():
    """Sample lifestyle factor data for testing."""
    return {
        "PatientID": 1,
        "BMI": 28.5,
        "Smoker": False,
        "PhysActivity": True,
        "Fruits": True,
        "Veggies": True,
        "HvyAlcoholConsump": False
    }


@pytest.fixture
def sample_health_metric_data():
    """Sample health metric data for testing."""
    return {
        "PatientID": 1,
        "CholCheck": True,
        "GenHlth": 3,
        "MentHlth": 5,
        "PhysHlth": 2
    }


@pytest.fixture
def sample_healthcare_access_data():
    """Sample healthcare access data for testing."""
    return {
        "PatientID": 1,
        "AnyHealthcare": True,
        "NoDocbcCost": False
    }
