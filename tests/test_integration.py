"""
Integration tests for the API.
Tests complete workflows across multiple endpoints.
"""
import pytest
from fastapi import status


class TestPostgresIntegration:
    """Integration tests for PostgreSQL endpoints."""
    
    def test_complete_patient_workflow(self, client, test_db):
        """Test creating patient with all related data."""
        # 1. Create patient
        patient_data = {
            "Sex": True,
            "Age": 45,
            "Education": 4,
            "Income": 75000
        }
        patient_response = client.post("/api/v1/postgres/patients/", json=patient_data)
        assert patient_response.status_code == status.HTTP_201_CREATED
        patient_id = patient_response.json()["PatientID"]
        
        # 2. Create health condition
        condition_data = {
            "PatientID": patient_id,
            "Diabetes_012": False,
            "HighBP": True,
            "HighChol": True,
            "Stroke": False,
            "HeartDiseaseorAttack": False,
            "DiffWalk": False
        }
        condition_response = client.post("/api/v1/postgres/health-conditions/", json=condition_data)
        assert condition_response.status_code == status.HTTP_201_CREATED
        condition_id = condition_response.json()["ConditionID"]
        
        # 3. Create lifestyle factor
        lifestyle_data = {
            "PatientID": patient_id,
            "BMI": 28.5,
            "Smoker": False,
            "PhysActivity": True,
            "Fruits": True,
            "Veggies": True,
            "HvyAlcoholConsump": False
        }
        lifestyle_response = client.post("/api/v1/postgres/lifestyle-factors/", json=lifestyle_data)
        assert lifestyle_response.status_code == status.HTTP_201_CREATED
        lifestyle_id = lifestyle_response.json()["LifestyleID"]
        
        # 4. Create health metric
        metric_data = {
            "PatientID": patient_id,
            "CholCheck": True,
            "GenHlth": 3,
            "MentHlth": 5,
            "PhysHlth": 2
        }
        metric_response = client.post("/api/v1/postgres/health-metrics/", json=metric_data)
        assert metric_response.status_code == status.HTTP_201_CREATED
        metric_id = metric_response.json()["MetricsID"]
        
        # 5. Create healthcare access
        access_data = {
            "PatientID": patient_id,
            "AnyHealthcare": True,
            "NoDocbcCost": False
        }
        access_response = client.post("/api/v1/postgres/healthcare-access/", json=access_data)
        assert access_response.status_code == status.HTTP_201_CREATED
        access_id = access_response.json()["AccessID"]
        
        # 6. Update patient
        update_patient = client.put(f"/api/v1/postgres/patients/{patient_id}", json={"Age": 46})
        assert update_patient.status_code == status.HTTP_200_OK
        assert update_patient.json()["Age"] == 46
        
        # 7. Update health condition (must include PatientID)
        update_condition = client.put(f"/api/v1/postgres/health-conditions/{condition_id}", json={"PatientID": patient_id, "HighBP": False})
        assert update_condition.status_code == status.HTTP_200_OK
        assert update_condition.json()["HighBP"] == False
        
        # 8. Delete all related records
        assert client.delete(f"/api/v1/postgres/healthcare-access/{access_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/postgres/health-metrics/{metric_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/postgres/lifestyle-factors/{lifestyle_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/postgres/health-conditions/{condition_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/postgres/patients/{patient_id}").status_code == status.HTTP_200_OK
    
    def test_cascade_delete_behavior(self, client, test_db):
        """Test that deleting a patient cascades to related records."""
        # Create patient
        patient_response = client.post("/api/v1/postgres/patients/", json={
            "Sex": True,
            "Age": 45,
            "Education": 4,
            "Income": 75000
        })
        patient_id = patient_response.json()["PatientID"]
        
        # Create health condition
        client.post("/api/v1/postgres/health-conditions/", json={
            "PatientID": patient_id,
            "Diabetes_012": False,
            "HighBP": True,
            "HighChol": True,
            "Stroke": False,
            "HeartDiseaseorAttack": False,
            "DiffWalk": False
        })
        
        # Delete patient (should cascade to health condition due to foreign key constraints)
        delete_response = client.delete(f"/api/v1/postgres/patients/{patient_id}")
        assert delete_response.status_code == status.HTTP_200_OK


class TestMongoDBIntegration:
    """Integration tests for MongoDB endpoints."""
    
    def test_complete_patient_workflow(self, client, test_mongo_db):
        """Test creating patient with all related data in MongoDB."""
        patient_id = 1
        
        # 1. Create patient
        patient_data = {
            "PatientID": patient_id,
            "Sex": True,
            "Age": 45,
            "Education": 4,
            "Income": 75000
        }
        patient_response = client.post("/api/v1/mongodb/patients/", json=patient_data)
        assert patient_response.status_code == status.HTTP_201_CREATED
        mongo_patient_id = patient_response.json()["_id"]
        
        # 2. Create health condition
        condition_data = {
            "PatientID": patient_id,
            "Diabetes_012": False,
            "HighBP": True,
            "HighChol": True,
            "Stroke": False,
            "HeartDiseaseorAttack": False,
            "DiffWalk": False
        }
        condition_response = client.post("/api/v1/mongodb/health-conditions/", json=condition_data)
        assert condition_response.status_code == status.HTTP_201_CREATED
        mongo_condition_id = condition_response.json()["_id"]
        
        # 3. Create lifestyle factor
        lifestyle_data = {
            "PatientID": patient_id,
            "BMI": 28.5,
            "Smoker": False,
            "PhysActivity": True,
            "Fruits": True,
            "Veggies": True,
            "HvyAlcoholConsump": False
        }
        lifestyle_response = client.post("/api/v1/mongodb/lifestyle-factors/", json=lifestyle_data)
        assert lifestyle_response.status_code == status.HTTP_201_CREATED
        mongo_lifestyle_id = lifestyle_response.json()["_id"]
        
        # 4. Update patient
        update_patient = client.put(f"/api/v1/mongodb/patients/{mongo_patient_id}", json={
            "PatientID": patient_id,
            "Age": 46
        })
        assert update_patient.status_code == status.HTTP_200_OK
        assert update_patient.json()["Age"] == 46
        
        # 5. Verify timestamps are updated
        assert "updated_at" in update_patient.json()
        
        # 6. Delete all records
        assert client.delete(f"/api/v1/mongodb/lifestyle-factors/{mongo_lifestyle_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/mongodb/health-conditions/{mongo_condition_id}").status_code == status.HTTP_200_OK
        assert client.delete(f"/api/v1/mongodb/patients/{mongo_patient_id}").status_code == status.HTTP_200_OK
    
    def test_multiple_patients_independent(self, client, test_mongo_db):
        """Test that multiple patients can be created and managed independently."""
        # Create first patient
        patient1 = client.post("/api/v1/mongodb/patients/", json={
            "PatientID": 1,
            "Sex": True,
            "Age": 30,
            "Education": 4,
            "Income": 60000
        })
        assert patient1.status_code == status.HTTP_201_CREATED
        patient1_id = patient1.json()["_id"]
        
        # Create second patient
        patient2 = client.post("/api/v1/mongodb/patients/", json={
            "PatientID": 2,
            "Sex": False,
            "Age": 40,
            "Education": 5,
            "Income": 80000
        })
        assert patient2.status_code == status.HTTP_201_CREATED
        patient2_id = patient2.json()["_id"]
        
        # Delete first patient
        delete1 = client.delete(f"/api/v1/mongodb/patients/{patient1_id}")
        assert delete1.status_code == status.HTTP_200_OK
        
        # Update second patient (should still work)
        update2 = client.put(f"/api/v1/mongodb/patients/{patient2_id}", json={
            "PatientID": 2,
            "Age": 41
        })
        assert update2.status_code == status.HTTP_200_OK
        assert update2.json()["Age"] == 41
        
        # Clean up
        client.delete(f"/api/v1/mongodb/patients/{patient2_id}")


class TestCrossDatabase:
    """Test interactions between PostgreSQL and MongoDB."""
    
    def test_same_patient_in_both_databases(self, client, test_db, test_mongo_db):
        """Test creating the same patient in both databases."""
        patient_data = {
            "Sex": True,
            "Age": 45,
            "Education": 4,
            "Income": 75000
        }
        
        # Create in PostgreSQL
        postgres_response = client.post("/api/v1/postgres/patients/", json=patient_data)
        assert postgres_response.status_code == status.HTTP_201_CREATED
        postgres_id = postgres_response.json()["PatientID"]
        
        # Create in MongoDB
        mongo_data = patient_data.copy()
        mongo_data["PatientID"] = postgres_id
        mongo_response = client.post("/api/v1/mongodb/patients/", json=mongo_data)
        assert mongo_response.status_code == status.HTTP_201_CREATED
        mongo_id = mongo_response.json()["_id"]
        
        # Update in both
        update_data_postgres = {"Age": 46}
        update_data_mongo = {"PatientID": postgres_id, "Age": 46}
        
        postgres_update = client.put(f"/api/v1/postgres/patients/{postgres_id}", json=update_data_postgres)
        mongo_update = client.put(f"/api/v1/mongodb/patients/{mongo_id}", json=update_data_mongo)
        
        assert postgres_update.status_code == status.HTTP_200_OK
        assert mongo_update.status_code == status.HTTP_200_OK
        assert postgres_update.json()["Age"] == 46
        assert mongo_update.json()["Age"] == 46
        
        # Clean up
        client.delete(f"/api/v1/postgres/patients/{postgres_id}")
        client.delete(f"/api/v1/mongodb/patients/{mongo_id}")
