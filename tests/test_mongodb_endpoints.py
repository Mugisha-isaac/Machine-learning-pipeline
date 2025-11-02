"""
Test cases for MongoDB API endpoints.
Tests POST, PUT, and DELETE operations for all entities.
"""
import pytest
from fastapi import status
from bson import ObjectId


class TestMongoDBPatientEndpoints:
    """Test cases for Patient endpoints in MongoDB."""
    
    def test_create_patient(self, client, test_mongo_db, sample_patient_data):
        """Test creating a new patient in MongoDB."""
        sample_patient_data["PatientID"] = 1
        response = client.post("/api/v1/mongodb/patients/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "_id" in data
        assert data["Age"] == sample_patient_data["Age"]
        assert data["Sex"] == sample_patient_data["Sex"]
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_update_patient(self, client, test_mongo_db, sample_patient_data):
        """Test updating an existing patient in MongoDB."""
        # Create a patient first
        sample_patient_data["PatientID"] = 1
        create_response = client.post("/api/v1/mongodb/patients/", json=sample_patient_data)
        patient_id = create_response.json()["_id"]
        
        # Update the patient
        update_data = {"PatientID": 1, "Age": 46, "Income": 80000}
        response = client.put(f"/api/v1/mongodb/patients/{patient_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["Age"] == 46
        assert data["Income"] == 80000
        assert "updated_at" in data
    
    def test_update_nonexistent_patient(self, client, test_mongo_db):
        """Test updating a patient that doesn't exist in MongoDB."""
        fake_id = str(ObjectId())
        response = client.put(f"/api/v1/mongodb/patients/{fake_id}", json={"PatientID": 1, "Age": 50})
        
        # MongoDB might return 500 or 404 depending on error handling
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_500_INTERNAL_SERVER_ERROR]
    
    def test_delete_patient(self, client, test_mongo_db, sample_patient_data):
        """Test deleting a patient from MongoDB."""
        # Create a patient first
        sample_patient_data["PatientID"] = 1
        create_response = client.post("/api/v1/mongodb/patients/", json=sample_patient_data)
        patient_id = create_response.json()["_id"]
        
        # Delete the patient
        response = client.delete(f"/api/v1/mongodb/patients/{patient_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
    
    def test_delete_nonexistent_patient(self, client, test_mongo_db):
        """Test deleting a patient that doesn't exist in MongoDB."""
        fake_id = str(ObjectId())
        response = client.delete(f"/api/v1/mongodb/patients/{fake_id}")
        
        # MongoDB might return 500 or 404 depending on error handling
        assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_500_INTERNAL_SERVER_ERROR]


class TestMongoDBHealthConditionEndpoints:
    """Test cases for Health Condition endpoints in MongoDB."""
    
    def test_create_health_condition(self, client, test_mongo_db, sample_health_condition_data):
        """Test creating a new health condition in MongoDB."""
        response = client.post("/api/v1/mongodb/health-conditions/", json=sample_health_condition_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "_id" in data
        assert data["PatientID"] == sample_health_condition_data["PatientID"]
        assert data["HighBP"] == sample_health_condition_data["HighBP"]
        assert "created_at" in data
    
    def test_update_health_condition(self, client, test_mongo_db, sample_health_condition_data):
        """Test updating a health condition in MongoDB."""
        # Create condition first
        create_response = client.post("/api/v1/mongodb/health-conditions/", json=sample_health_condition_data)
        condition_id = create_response.json()["_id"]
        
        # Update the condition
        update_data = {"PatientID": 1, "HighBP": False, "Stroke": True}
        response = client.put(f"/api/v1/mongodb/health-conditions/{condition_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["HighBP"] == False
        assert data["Stroke"] == True
    
    def test_delete_health_condition(self, client, test_mongo_db, sample_health_condition_data):
        """Test deleting a health condition from MongoDB."""
        # Create condition first
        create_response = client.post("/api/v1/mongodb/health-conditions/", json=sample_health_condition_data)
        condition_id = create_response.json()["_id"]
        
        # Delete the condition
        response = client.delete(f"/api/v1/mongodb/health-conditions/{condition_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestMongoDBLifestyleFactorEndpoints:
    """Test cases for Lifestyle Factor endpoints in MongoDB."""
    
    def test_create_lifestyle_factor(self, client, test_mongo_db, sample_lifestyle_factor_data):
        """Test creating a new lifestyle factor in MongoDB."""
        response = client.post("/api/v1/mongodb/lifestyle-factors/", json=sample_lifestyle_factor_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "_id" in data
        assert data["BMI"] == sample_lifestyle_factor_data["BMI"]
        assert data["Smoker"] == sample_lifestyle_factor_data["Smoker"]
    
    def test_update_lifestyle_factor(self, client, test_mongo_db, sample_lifestyle_factor_data):
        """Test updating a lifestyle factor in MongoDB."""
        # Create lifestyle factor first
        create_response = client.post("/api/v1/mongodb/lifestyle-factors/", json=sample_lifestyle_factor_data)
        lifestyle_id = create_response.json()["_id"]
        
        # Update the lifestyle factor
        update_data = {"PatientID": 1, "BMI": 30.0, "Smoker": True}
        response = client.put(f"/api/v1/mongodb/lifestyle-factors/{lifestyle_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["BMI"] == 30.0
        assert data["Smoker"] == True
    
    def test_delete_lifestyle_factor(self, client, test_mongo_db, sample_lifestyle_factor_data):
        """Test deleting a lifestyle factor from MongoDB."""
        # Create lifestyle factor first
        create_response = client.post("/api/v1/mongodb/lifestyle-factors/", json=sample_lifestyle_factor_data)
        lifestyle_id = create_response.json()["_id"]
        
        # Delete the lifestyle factor
        response = client.delete(f"/api/v1/mongodb/lifestyle-factors/{lifestyle_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestMongoDBHealthMetricEndpoints:
    """Test cases for Health Metric endpoints in MongoDB."""
    
    def test_create_health_metric(self, client, test_mongo_db, sample_health_metric_data):
        """Test creating a new health metric in MongoDB."""
        response = client.post("/api/v1/mongodb/health-metrics/", json=sample_health_metric_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "_id" in data
        assert data["GenHlth"] == sample_health_metric_data["GenHlth"]
    
    def test_update_health_metric(self, client, test_mongo_db, sample_health_metric_data):
        """Test updating a health metric in MongoDB."""
        # Create health metric first
        create_response = client.post("/api/v1/mongodb/health-metrics/", json=sample_health_metric_data)
        metric_id = create_response.json()["_id"]
        
        # Update the health metric
        update_data = {"PatientID": 1, "GenHlth": 4, "MentHlth": 10}
        response = client.put(f"/api/v1/mongodb/health-metrics/{metric_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["GenHlth"] == 4
        assert data["MentHlth"] == 10
    
    def test_delete_health_metric(self, client, test_mongo_db, sample_health_metric_data):
        """Test deleting a health metric from MongoDB."""
        # Create health metric first
        create_response = client.post("/api/v1/mongodb/health-metrics/", json=sample_health_metric_data)
        metric_id = create_response.json()["_id"]
        
        # Delete the health metric
        response = client.delete(f"/api/v1/mongodb/health-metrics/{metric_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestMongoDBHealthcareAccessEndpoints:
    """Test cases for Healthcare Access endpoints in MongoDB."""
    
    def test_create_healthcare_access(self, client, test_mongo_db, sample_healthcare_access_data):
        """Test creating a new healthcare access record in MongoDB."""
        response = client.post("/api/v1/mongodb/healthcare-access/", json=sample_healthcare_access_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "_id" in data
        assert data["AnyHealthcare"] == sample_healthcare_access_data["AnyHealthcare"]
    
    def test_update_healthcare_access(self, client, test_mongo_db, sample_healthcare_access_data):
        """Test updating a healthcare access record in MongoDB."""
        # Create healthcare access first
        create_response = client.post("/api/v1/mongodb/healthcare-access/", json=sample_healthcare_access_data)
        access_id = create_response.json()["_id"]
        
        # Update the healthcare access
        update_data = {"PatientID": 1, "AnyHealthcare": False, "NoDocbcCost": True}
        response = client.put(f"/api/v1/mongodb/healthcare-access/{access_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["AnyHealthcare"] == False
        assert data["NoDocbcCost"] == True
    
    def test_delete_healthcare_access(self, client, test_mongo_db, sample_healthcare_access_data):
        """Test deleting a healthcare access record from MongoDB."""
        # Create healthcare access first
        create_response = client.post("/api/v1/mongodb/healthcare-access/", json=sample_healthcare_access_data)
        access_id = create_response.json()["_id"]
        
        # Delete the healthcare access
        response = client.delete(f"/api/v1/mongodb/healthcare-access/{access_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()


class TestMongoDBValidation:
    """Test data validation and error handling for MongoDB endpoints."""
    
    def test_create_patient_with_invalid_objectid(self, client, test_mongo_db):
        """Test updating with an invalid ObjectId."""
        invalid_id = "not_a_valid_objectid"
        response = client.put(f"/api/v1/mongodb/patients/{invalid_id}", json={"PatientID": 1, "Age": 50})
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def test_create_patient_with_invalid_data(self, client, test_mongo_db):
        """Test creating a patient with invalid data types."""
        invalid_data = {
            "PatientID": "not_a_number",  # Should be int
            "Sex": "invalid",  # Should be boolean
            "Age": "not_a_number",
            "Education": 4,
            "Income": 75000
        }
        response = client.post("/api/v1/mongodb/patients/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_timestamps_are_added(self, client, test_mongo_db, sample_patient_data):
        """Test that created_at and updated_at timestamps are automatically added."""
        sample_patient_data["PatientID"] = 1
        response = client.post("/api/v1/mongodb/patients/", json=sample_patient_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_updated_at_changes_on_update(self, client, test_mongo_db, sample_patient_data):
        """Test that updated_at timestamp changes when updating a document."""
        sample_patient_data["PatientID"] = 1
        create_response = client.post("/api/v1/mongodb/patients/", json=sample_patient_data)
        patient_id = create_response.json()["_id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Wait a moment and update
        import time
        time.sleep(0.1)
        
        update_data = {"PatientID": 1, "Age": 50}
        update_response = client.put(f"/api/v1/mongodb/patients/{patient_id}", json=update_data)
        
        assert update_response.status_code == status.HTTP_200_OK
        new_updated_at = update_response.json()["updated_at"]
        assert new_updated_at != original_updated_at
