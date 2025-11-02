"""
Test cases for PostgreSQL API endpoints.
Tests POST, PUT, and DELETE operations for all entities.
"""
import pytest
from fastapi import status


class TestPostgresPatientEndpoints:
    """Test cases for Patient endpoints."""
    
    def test_create_patient(self, client, test_db, sample_patient_data):
        """Test creating a new patient."""
        response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "PatientID" in data
        assert data["Age"] == sample_patient_data["Age"]
        assert data["Sex"] == sample_patient_data["Sex"]
        assert data["Education"] == sample_patient_data["Education"]
        assert data["Income"] == sample_patient_data["Income"]
    
    def test_update_patient(self, client, test_db, sample_patient_data):
        """Test updating an existing patient."""
        # Create a patient first
        create_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = create_response.json()["PatientID"]
        
        # Update the patient
        update_data = {"Age": 46, "Income": 80000}
        response = client.put(f"/api/v1/postgres/patients/{patient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["Age"] == 46
        assert data["Income"] == 80000
        assert data["PatientID"] == patient_id
    
    def test_update_nonexistent_patient(self, client, test_db):
        """Test updating a patient that doesn't exist."""
        response = client.put("/api/v1/postgres/patients/99999", json={"Age": 50})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_patient(self, client, test_db, sample_patient_data):
        """Test deleting a patient."""
        # Create a patient first
        create_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = create_response.json()["PatientID"]
        
        # Delete the patient
        response = client.delete(f"/api/v1/postgres/patients/{patient_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
    
    def test_delete_nonexistent_patient(self, client, test_db):
        """Test deleting a patient that doesn't exist."""
        response = client.delete("/api/v1/postgres/patients/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPostgresHealthConditionEndpoints:
    """Test cases for Health Condition endpoints."""
    
    def test_create_health_condition(self, client, test_db, sample_patient_data, sample_health_condition_data):
        """Test creating a new health condition."""
        # Create a patient first
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        # Create health condition
        sample_health_condition_data["PatientID"] = patient_id
        response = client.post("/api/v1/postgres/health-conditions/", json=sample_health_condition_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "ConditionID" in data
        assert data["PatientID"] == patient_id
        assert data["HighBP"] == sample_health_condition_data["HighBP"]
    
    def test_update_health_condition(self, client, test_db, sample_patient_data, sample_health_condition_data):
        """Test updating a health condition."""
        # Create patient and condition
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_health_condition_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/health-conditions/", json=sample_health_condition_data)
        condition_id = create_response.json()["ConditionID"]
        
        # Update the condition (must include PatientID)
        update_data = {"PatientID": patient_id, "HighBP": False, "Stroke": True}
        response = client.put(f"/api/v1/postgres/health-conditions/{condition_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["HighBP"] == False
        assert data["Stroke"] == True
    
    def test_delete_health_condition(self, client, test_db, sample_patient_data, sample_health_condition_data):
        """Test deleting a health condition."""
        # Create patient and condition
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_health_condition_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/health-conditions/", json=sample_health_condition_data)
        condition_id = create_response.json()["ConditionID"]
        
        # Delete the condition
        response = client.delete(f"/api/v1/postgres/health-conditions/{condition_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestPostgresLifestyleFactorEndpoints:
    """Test cases for Lifestyle Factor endpoints."""
    
    def test_create_lifestyle_factor(self, client, test_db, sample_patient_data, sample_lifestyle_factor_data):
        """Test creating a new lifestyle factor."""
        # Create a patient first
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        # Create lifestyle factor
        sample_lifestyle_factor_data["PatientID"] = patient_id
        response = client.post("/api/v1/postgres/lifestyle-factors/", json=sample_lifestyle_factor_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "LifestyleID" in data
        assert data["BMI"] == sample_lifestyle_factor_data["BMI"]
        assert data["Smoker"] == sample_lifestyle_factor_data["Smoker"]
    
    def test_update_lifestyle_factor(self, client, test_db, sample_patient_data, sample_lifestyle_factor_data):
        """Test updating a lifestyle factor."""
        # Create patient and lifestyle factor
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_lifestyle_factor_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/lifestyle-factors/", json=sample_lifestyle_factor_data)
        lifestyle_id = create_response.json()["LifestyleID"]
        
        # Update the lifestyle factor (must include PatientID)
        update_data = {"PatientID": patient_id, "BMI": 30.0, "Smoker": True}
        response = client.put(f"/api/v1/postgres/lifestyle-factors/{lifestyle_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["BMI"] == 30.0
        assert data["Smoker"] == True
    
    def test_delete_lifestyle_factor(self, client, test_db, sample_patient_data, sample_lifestyle_factor_data):
        """Test deleting a lifestyle factor."""
        # Create patient and lifestyle factor
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_lifestyle_factor_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/lifestyle-factors/", json=sample_lifestyle_factor_data)
        lifestyle_id = create_response.json()["LifestyleID"]
        
        # Delete the lifestyle factor
        response = client.delete(f"/api/v1/postgres/lifestyle-factors/{lifestyle_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestPostgresHealthMetricEndpoints:
    """Test cases for Health Metric endpoints."""
    
    def test_create_health_metric(self, client, test_db, sample_patient_data, sample_health_metric_data):
        """Test creating a new health metric."""
        # Create a patient first
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        # Create health metric
        sample_health_metric_data["PatientID"] = patient_id
        response = client.post("/api/v1/postgres/health-metrics/", json=sample_health_metric_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "MetricsID" in data
        assert data["GenHlth"] == sample_health_metric_data["GenHlth"]
    
    def test_update_health_metric(self, client, test_db, sample_patient_data, sample_health_metric_data):
        """Test updating a health metric."""
        # Create patient and health metric
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_health_metric_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/health-metrics/", json=sample_health_metric_data)
        metric_id = create_response.json()["MetricsID"]
        
        # Update the health metric (must include PatientID)
        update_data = {"PatientID": patient_id, "GenHlth": 4, "MentHlth": 10}
        response = client.put(f"/api/v1/postgres/health-metrics/{metric_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["GenHlth"] == 4
        assert data["MentHlth"] == 10
    
    def test_delete_health_metric(self, client, test_db, sample_patient_data, sample_health_metric_data):
        """Test deleting a health metric."""
        # Create patient and health metric
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_health_metric_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/health-metrics/", json=sample_health_metric_data)
        metric_id = create_response.json()["MetricsID"]
        
        # Delete the health metric
        response = client.delete(f"/api/v1/postgres/health-metrics/{metric_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestPostgresHealthcareAccessEndpoints:
    """Test cases for Healthcare Access endpoints."""
    
    def test_create_healthcare_access(self, client, test_db, sample_patient_data, sample_healthcare_access_data):
        """Test creating a new healthcare access record."""
        # Create a patient first
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        # Create healthcare access
        sample_healthcare_access_data["PatientID"] = patient_id
        response = client.post("/api/v1/postgres/healthcare-access/", json=sample_healthcare_access_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "AccessID" in data
        assert data["AnyHealthcare"] == sample_healthcare_access_data["AnyHealthcare"]
    
    def test_update_healthcare_access(self, client, test_db, sample_patient_data, sample_healthcare_access_data):
        """Test updating a healthcare access record."""
        # Create patient and healthcare access
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_healthcare_access_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/healthcare-access/", json=sample_healthcare_access_data)
        access_id = create_response.json()["AccessID"]
        
        # Update the healthcare access (must include PatientID)
        update_data = {"PatientID": patient_id, "AnyHealthcare": False, "NoDocbcCost": True}
        response = client.put(f"/api/v1/postgres/healthcare-access/{access_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["AnyHealthcare"] == False
        assert data["NoDocbcCost"] == True
    
    def test_delete_healthcare_access(self, client, test_db, sample_patient_data, sample_healthcare_access_data):
        """Test deleting a healthcare access record."""
        # Create patient and healthcare access
        patient_response = client.post("/api/v1/postgres/patients/", json=sample_patient_data)
        patient_id = patient_response.json()["PatientID"]
        
        sample_healthcare_access_data["PatientID"] = patient_id
        create_response = client.post("/api/v1/postgres/healthcare-access/", json=sample_healthcare_access_data)
        access_id = create_response.json()["AccessID"]
        
        # Delete the healthcare access
        response = client.delete(f"/api/v1/postgres/healthcare-access/{access_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestPostgresValidation:
    """Test data validation for PostgreSQL endpoints."""
    
    def test_create_patient_with_invalid_data(self, client, test_db):
        """Test creating a patient with invalid data types."""
        invalid_data = {
            "Sex": "invalid",  # Should be boolean
            "Age": "not_a_number",  # Should be int
            "Education": 4,
            "Income": 75000
        }
        response = client.post("/api/v1/postgres/patients/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_health_condition_without_patient(self, client, test_db, sample_health_condition_data):
        """Test creating a health condition without a valid patient."""
        sample_health_condition_data["PatientID"] = 99999
        response = client.post("/api/v1/postgres/health-conditions/", json=sample_health_condition_data)
        
        # Should fail - accepting either 500 (foreign key constraint) or 400 (validation)
        assert response.status_code in [status.HTTP_500_INTERNAL_SERVER_ERROR, status.HTTP_400_BAD_REQUEST]
