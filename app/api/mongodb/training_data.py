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
    description="Retrieve latest patient records with all related health data joined together"
)
def get_latest_training_data(limit: int = 100):
    """
    Get the most recent patient records with all related information for ML model training.
    Returns complete flattened dataset including demographics, health conditions, lifestyle factors,
    health metrics, and healthcare access information.
    """
    try:
        db = get_mongo_db()
        
        # Get latest patients
        patients = list(
            db[COLLECTIONS["patients"]].find().sort("updated_at", -1).limit(limit)
        )
        
        training_data = []
        for patient in patients:
            patient_id = patient.get("PatientID")
            
            # Get related data for each patient
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
            "records": training_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/training-data/complete",
    summary="Get complete patient records for ML model training",
    description="Retrieve patient records that have all related data (no null values)"
)
def get_complete_training_data(skip: int = 0, limit: int = 1000):
    """
    Get patient records with complete data across all collections for ML model training.
    Only returns patients who have entries in all related collections with no null critical fields.
    """
    try:
        db = get_mongo_db()
        
        # Use aggregation pipeline to join all collections
        pipeline = [
            # Sort by updated_at descending
            {"$sort": {"updated_at": -1}},
            # Skip and limit
            {"$skip": skip},
            {"$limit": limit},
            # Lookup health conditions
            {
                "$lookup": {
                    "from": COLLECTIONS["health_conditions"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "health_conditions"
                }
            },
            # Lookup lifestyle factors
            {
                "$lookup": {
                    "from": COLLECTIONS["lifestyle_factors"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "lifestyle_factors"
                }
            },
            # Lookup health metrics
            {
                "$lookup": {
                    "from": COLLECTIONS["health_metrics"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "health_metrics"
                }
            },
            # Lookup healthcare access
            {
                "$lookup": {
                    "from": COLLECTIONS["healthcare_access"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "healthcare_access"
                }
            },
            # Filter to only include patients with all related data
            {
                "$match": {
                    "health_conditions": {"$ne": []},
                    "lifestyle_factors": {"$ne": []},
                    "health_metrics": {"$ne": []},
                    "healthcare_access": {"$ne": []}
                }
            }
        ]
        
        results = list(db[COLLECTIONS["patients"]].aggregate(pipeline))
        
        training_data = []
        for patient in results:
            # Get first element from each array (assuming one-to-one relationship)
            condition = patient["health_conditions"][0] if patient.get("health_conditions") else {}
            lifestyle = patient["lifestyle_factors"][0] if patient.get("lifestyle_factors") else {}
            metric = patient["health_metrics"][0] if patient.get("health_metrics") else {}
            access = patient["healthcare_access"][0] if patient.get("healthcare_access") else {}
            
            # Flatten the record
            record = {
                "_id": str(patient["_id"]),
                "PatientID": patient.get("PatientID"),
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
        
        # Get total count of complete records
        count_pipeline = [
            {
                "$lookup": {
                    "from": COLLECTIONS["health_conditions"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "health_conditions"
                }
            },
            {
                "$lookup": {
                    "from": COLLECTIONS["lifestyle_factors"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "lifestyle_factors"
                }
            },
            {
                "$lookup": {
                    "from": COLLECTIONS["health_metrics"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "health_metrics"
                }
            },
            {
                "$lookup": {
                    "from": COLLECTIONS["healthcare_access"],
                    "localField": "PatientID",
                    "foreignField": "PatientID",
                    "as": "healthcare_access"
                }
            },
            {
                "$match": {
                    "health_conditions": {"$ne": []},
                    "lifestyle_factors": {"$ne": []},
                    "health_metrics": {"$ne": []},
                    "healthcare_access": {"$ne": []}
                }
            },
            {"$count": "total"}
        ]
        
        count_result = list(db[COLLECTIONS["patients"]].aggregate(count_pipeline))
        total_count = count_result[0]["total"] if count_result else 0
        
        return {
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "returned": len(training_data),
            "records": training_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
