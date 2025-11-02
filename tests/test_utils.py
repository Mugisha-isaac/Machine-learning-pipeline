"""
Utility functions for testing.
"""
from typing import Dict, Any
import random
from datetime import datetime


def generate_patient_data(override: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate random patient data for testing."""
    data = {
        "Sex": random.choice([True, False]),
        "Age": random.randint(18, 90),
        "Education": random.randint(1, 6),
        "Income": random.randint(20000, 150000)
    }
    if override:
        data.update(override)
    return data


def generate_health_condition_data(patient_id: int, override: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate random health condition data for testing."""
    data = {
        "PatientID": patient_id,
        "Diabetes_012": random.choice([True, False]),
        "HighBP": random.choice([True, False]),
        "HighChol": random.choice([True, False]),
        "Stroke": random.choice([True, False]),
        "HeartDiseaseorAttack": random.choice([True, False]),
        "DiffWalk": random.choice([True, False])
    }
    if override:
        data.update(override)
    return data


def generate_lifestyle_factor_data(patient_id: int, override: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate random lifestyle factor data for testing."""
    data = {
        "PatientID": patient_id,
        "BMI": round(random.uniform(18.0, 40.0), 1),
        "Smoker": random.choice([True, False]),
        "PhysActivity": random.choice([True, False]),
        "Fruits": random.choice([True, False]),
        "Veggies": random.choice([True, False]),
        "HvyAlcoholConsump": random.choice([True, False])
    }
    if override:
        data.update(override)
    return data


def generate_health_metric_data(patient_id: int, override: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate random health metric data for testing."""
    data = {
        "PatientID": patient_id,
        "CholCheck": random.choice([True, False]),
        "GenHlth": random.randint(1, 5),
        "MentHlth": random.randint(0, 30),
        "PhysHlth": random.randint(0, 30)
    }
    if override:
        data.update(override)
    return data


def generate_healthcare_access_data(patient_id: int, override: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate random healthcare access data for testing."""
    data = {
        "PatientID": patient_id,
        "AnyHealthcare": random.choice([True, False]),
        "NoDocbcCost": random.choice([True, False])
    }
    if override:
        data.update(override)
    return data


def assert_patient_response(response_data: Dict[str, Any], expected_data: Dict[str, Any]):
    """Assert that patient response matches expected data."""
    assert "PatientID" in response_data or "_id" in response_data
    for key, value in expected_data.items():
        if key in response_data:
            assert response_data[key] == value, f"Expected {key}={value}, got {response_data[key]}"


def assert_timestamps_exist(response_data: Dict[str, Any]):
    """Assert that MongoDB timestamps exist in response."""
    assert "created_at" in response_data, "created_at timestamp missing"
    assert "updated_at" in response_data, "updated_at timestamp missing"
