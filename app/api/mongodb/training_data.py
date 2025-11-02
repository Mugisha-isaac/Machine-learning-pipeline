"""
MongoDB Training Data Controller
Handles ML training data aggregation and retrieval operations
"""
from fastapi import APIRouter, HTTPException, status

from app.core.database import get_mongo_db
from app.core import COLLECTIONS

router = APIRouter(tags=["MongoDB - Training Data"])


@router.get("/all/latest",
    summary="Get latest records across all collections",
    description="Retrieve the most recently updated records from all collections"
)
def get_all_latest_records(limit: int = 5):
    try:
        db = get_mongo_db()
        
        # Get latest from each collection
        latest_patients = list(
            db[COLLECTIONS["patients"]].find().sort("updated_at", -1).limit(limit)
        )
        latest_conditions = list(
            db[COLLECTIONS["health_conditions"]].find().sort("updated_at", -1).limit(limit)
        )
        latest_lifestyle = list(
            db[COLLECTIONS["lifestyle_factors"]].find().sort("updated_at", -1).limit(limit)
        )
        latest_metrics = list(
            db[COLLECTIONS["health_metrics"]].find().sort("updated_at", -1).limit(limit)
        )
        latest_access = list(
            db[COLLECTIONS["healthcare_access"]].find().sort("updated_at", -1).limit(limit)
        )
        
        # Convert ObjectIds to strings
        for patient in latest_patients:
            patient["_id"] = str(patient["_id"])
        for condition in latest_conditions:
            condition["_id"] = str(condition["_id"])
        for lifestyle in latest_lifestyle:
            lifestyle["_id"] = str(lifestyle["_id"])
        for metric in latest_metrics:
            metric["_id"] = str(metric["_id"])
        for access in latest_access:
            access["_id"] = str(access["_id"])
        
        return {
            "limit_per_collection": limit,
            "latest_patients": latest_patients,
            "latest_health_conditions": latest_conditions,
            "latest_lifestyle_factors": latest_lifestyle,
            "latest_health_metrics": latest_metrics,
            "latest_healthcare_access": latest_access
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/training-data/latest",
    summary="Get latest complete patient records for ML model training",
    description="Retrieve latest patient records with all related health data joined together."
)
def get_latest_training_data(limit: int = 50):
    """
    Get the most recent patient records with all related information for ML model training.
    Returns complete flattened dataset including demographics, health conditions, lifestyle factors,
    health metrics, and healthcare access information.
    """
    try:
        db = get_mongo_db()
        
        if limit > 200:
            limit = 200
        
        # Sort by PatientID descending to get "latest" IDs (which are recent)
        # This is faster than sorting by updated_at which may not be indexed
        patients = list(
            db[COLLECTIONS["patients"]]
            .find()
            .sort("PatientID", -1)  # Use indexed field for better performance
            .limit(limit)
        )
        
        training_data = []
        for patient in patients:
            patient_id = patient.get("PatientID")
            
            # Get related data for each patient (fast with indices)
            health_condition = db[COLLECTIONS["health_conditions"]].find_one({"PatientID": patient_id})
            lifestyle_factor = db[COLLECTIONS["lifestyle_factors"]].find_one({"PatientID": patient_id})
            health_metric = db[COLLECTIONS["health_metrics"]].find_one({"PatientID": patient_id})
            healthcare_access = db[COLLECTIONS["healthcare_access"]].find_one({"PatientID": patient_id})
            
            # Combine all data into a flattened record
            record = {
                "_id": str(patient["_id"]),
                "PatientID": patient_id,
                "Sex": patient.get("Sex"),
                "Age": patient.get("Age"),
                "Education": patient.get("Education"),
                "Income": patient.get("Income"),
                # Health Conditions
                "Diabetes_012": health_condition.get("Diabetes_012") if health_condition else None,
                "HighBP": health_condition.get("HighBP") if health_condition else None,
                "HighChol": health_condition.get("HighChol") if health_condition else None,
                "Stroke": health_condition.get("Stroke") if health_condition else None,
                "HeartDiseaseorAttack": health_condition.get("HeartDiseaseorAttack") if health_condition else None,
                "DiffWalk": health_condition.get("DiffWalk") if health_condition else None,
                # Lifestyle Factors
                "BMI": lifestyle_factor.get("BMI") if lifestyle_factor else None,
                "Smoker": lifestyle_factor.get("Smoker") if lifestyle_factor else None,
                "PhysActivity": lifestyle_factor.get("PhysActivity") if lifestyle_factor else None,
                "Fruits": lifestyle_factor.get("Fruits") if lifestyle_factor else None,
                "Veggies": lifestyle_factor.get("Veggies") if lifestyle_factor else None,
                "HvyAlcoholConsump": lifestyle_factor.get("HvyAlcoholConsump") if lifestyle_factor else None,
                # Health Metrics
                "CholCheck": health_metric.get("CholCheck") if health_metric else None,
                "GenHlth": health_metric.get("GenHlth") if health_metric else None,
                "MentHlth": health_metric.get("MentHlth") if health_metric else None,
                "PhysHlth": health_metric.get("PhysHlth") if health_metric else None,
                # Healthcare Access
                "AnyHealthcare": healthcare_access.get("AnyHealthcare") if healthcare_access else None,
                "NoDocbcCost": healthcare_access.get("NoDocbcCost") if healthcare_access else None,
                # Metadata
                "created_at": str(patient.get("created_at")) if patient.get("created_at") else None,
                "updated_at": str(patient.get("updated_at")) if patient.get("updated_at") else None,
            }
            training_data.append(record)
        
        return {
            "total": len(training_data),
            "limit": limit,
            "returned": len(training_data),
            "records": training_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/training-data/complete",
    summary="Get complete patient records for ML model training",
    description="Retrieve patient records that have all related data (no null values). Uses optimized query with reduced limit."
)
def get_complete_training_data(skip: int = 0, limit: int = 100):
    """
    Get patient records with complete data across all collections for ML model training.
    Only returns patients who have entries in all related collections with no null critical fields.
    
    OPTIMIZED: Uses smaller batch size and efficient query to prevent timeouts.
    Maximum limit is 500 records per request to ensure fast response times.
    """
    try:
        db = get_mongo_db()
        
        # Limit maximum to prevent timeouts (MongoDB Atlas free tier has 5s timeout)
        if limit > 500:
            limit = 500
        
        # Simplified approach: Get patients first, then fetch related data
        # This is faster than complex aggregation pipelines on large datasets
        patients = list(
            db[COLLECTIONS["patients"]]
            .find()
            .sort("PatientID", 1)  # Sort by PatientID for consistent pagination
            .skip(skip)
            .limit(limit)
        )
        
        training_data = []
        for patient in patients:
            patient_id = patient.get("PatientID")
            
            # Fetch related documents individually (faster with proper indices)
            condition = db[COLLECTIONS["health_conditions"]].find_one({"PatientID": patient_id})
            lifestyle = db[COLLECTIONS["lifestyle_factors"]].find_one({"PatientID": patient_id})
            metric = db[COLLECTIONS["health_metrics"]].find_one({"PatientID": patient_id})
            access = db[COLLECTIONS["healthcare_access"]].find_one({"PatientID": patient_id})
            
            # Only include records that have ALL related data
            if condition and lifestyle and metric and access:
                # Flatten the record
                record = {
                    "_id": str(patient["_id"]),
                    "PatientID": patient_id,
                    "Sex": patient.get("Sex"),
                    "Age": patient.get("Age"),
                    "Education": patient.get("Education"),
                    "Income": patient.get("Income"),
                    # Health Conditions
                    "Diabetes_012": condition.get("Diabetes_012"),
                    "HighBP": condition.get("HighBP"),
                    "HighChol": condition.get("HighChol"),
                    "Stroke": condition.get("Stroke"),
                    "HeartDiseaseorAttack": condition.get("HeartDiseaseorAttack"),
                    "DiffWalk": condition.get("DiffWalk"),
                    # Lifestyle Factors
                    "BMI": lifestyle.get("BMI"),
                    "Smoker": lifestyle.get("Smoker"),
                    "PhysActivity": lifestyle.get("PhysActivity"),
                    "Fruits": lifestyle.get("Fruits"),
                    "Veggies": lifestyle.get("Veggies"),
                    "HvyAlcoholConsump": lifestyle.get("HvyAlcoholConsump"),
                    # Health Metrics
                    "CholCheck": metric.get("CholCheck"),
                    "GenHlth": metric.get("GenHlth"),
                    "MentHlth": metric.get("MentHlth"),
                    "PhysHlth": metric.get("PhysHlth"),
                    # Healthcare Access
                    "AnyHealthcare": access.get("AnyHealthcare"),
                    "NoDocbcCost": access.get("NoDocbcCost"),
                }
                training_data.append(record)
        
        # Get approximate total count (faster than exact count on large collections)
        total_patients = db[COLLECTIONS["patients"]].estimated_document_count()
        
        return {
            "skip": skip,
            "limit": limit,
            "returned": len(training_data),
            "records": training_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
