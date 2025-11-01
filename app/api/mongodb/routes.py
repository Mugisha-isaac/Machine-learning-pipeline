from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(
    prefix="/mongodb",
    tags=["MongoDB Operations"],
    responses={404: {"description": "Not found"}},
)

# ==================== PATIENT ENDPOINTS ====================

@router.get("/patients/",
    summary="Get all patients",
    description="Retrieve all patient records with optional pagination"
)
def get_all_patients(skip: int = 0, limit: int = 100):
    try:
        db = get_mongo_db()
        patients = list(db[COLLECTIONS["patients"]].find().skip(skip).limit(limit))
        
        for patient in patients:
            patient["_id"] = str(patient["_id"])
        
        return {
            "total": db[COLLECTIONS["patients"]].count_documents({}),
            "skip": skip,
            "limit": limit,
            "patients": patients
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patients/latest",
    summary="Get latest patients",
    description="Retrieve the most recently created or updated patient records"
)
def get_latest_patients(limit: int = 10):
    try:
        db = get_mongo_db()
        patients = list(
            db[COLLECTIONS["patients"]]
            .find()
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        for patient in patients:
            patient["_id"] = str(patient["_id"])
        
        return {
            "limit": limit,
            "count": len(patients),
            "patients": patients
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patients/by-patient-id/{patient_id}",
    summary="Get patient by PatientID",
    description="Retrieve patient record by PatientID field"
)
def get_patient_by_patient_id(patient_id: int):
    try:
        db = get_mongo_db()
        patient = db[COLLECTIONS["patients"]].find_one({"PatientID": patient_id})
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient["_id"] = str(patient["_id"])
        return patient
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patients/{patient_id}",
    summary="Get patient by ID",
    description="Retrieve a single patient record by ID"
)
def get_patient_by_id(patient_id: str):
    try:
        db = get_mongo_db()
        patient = db[COLLECTIONS["patients"]].find_one({"_id": ObjectId(patient_id)})
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient["_id"] = str(patient["_id"])
        return patient
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/patients/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient",
    description="Create a new patient record in MongoDB"
)
def create_patient(patient: mongo_models.Patient):
    try:
        db = get_mongo_db()
        patient_dict = patient.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        patient_dict["created_at"] = datetime.utcnow()
        patient_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["patients"]].insert_one(patient_dict)
        patient_dict["_id"] = str(result.inserted_id)
        return patient_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: mongo_models.Patient):
    try:
        db = get_mongo_db()
        patient_dict = patient.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        patient_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["patients"]].update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": patient_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        updated_patient = db[COLLECTIONS["patients"]].find_one({"_id": ObjectId(patient_id)})
        updated_patient["_id"] = str(updated_patient["_id"])
        return updated_patient
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    try:
        db = get_mongo_db()
        result = db[COLLECTIONS["patients"]].delete_one({"_id": ObjectId(patient_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== HEALTH CONDITION ENDPOINTS ====================

@router.get("/health-conditions/",
    summary="Get all health conditions",
    description="Retrieve all health condition records with optional pagination"
)
def get_all_health_conditions(skip: int = 0, limit: int = 100):
    try:
        db = get_mongo_db()
        conditions = list(db[COLLECTIONS["health_conditions"]].find().skip(skip).limit(limit))
        
        for condition in conditions:
            condition["_id"] = str(condition["_id"])
        
        return {
            "total": db[COLLECTIONS["health_conditions"]].count_documents({}),
            "skip": skip,
            "limit": limit,
            "health_conditions": conditions
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-conditions/latest",
    summary="Get latest health conditions",
    description="Retrieve the most recently created or updated health condition records"
)
def get_latest_health_conditions(limit: int = 10):
    try:
        db = get_mongo_db()
        conditions = list(
            db[COLLECTIONS["health_conditions"]]
            .find()
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        for condition in conditions:
            condition["_id"] = str(condition["_id"])
        
        return {
            "limit": limit,
            "count": len(conditions),
            "health_conditions": conditions
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-conditions/patient/{patient_id}",
    summary="Get health conditions by PatientID",
    description="Retrieve all health conditions for a specific patient"
)
def get_health_conditions_by_patient(patient_id: int):
    try:
        db = get_mongo_db()
        conditions = list(db[COLLECTIONS["health_conditions"]].find({"PatientID": patient_id}))
        
        for condition in conditions:
            condition["_id"] = str(condition["_id"])
        
        return {
            "PatientID": patient_id,
            "total": len(conditions),
            "health_conditions": conditions
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-conditions/{condition_id}",
    summary="Get health condition by ID",
    description="Retrieve a single health condition record by ID"
)
def get_health_condition_by_id(condition_id: str):
    try:
        db = get_mongo_db()
        condition = db[COLLECTIONS["health_conditions"]].find_one({"_id": ObjectId(condition_id)})
        
        if not condition:
            raise HTTPException(status_code=404, detail="Health condition not found")
        
        condition["_id"] = str(condition["_id"])
        return condition
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/health-conditions/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health condition",
    description="Create a new health condition record in MongoDB"
)
def create_health_condition(condition: mongo_models.HealthCondition):
    try:
        db = get_mongo_db()
        condition_dict = condition.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        condition_dict["created_at"] = datetime.utcnow()
        condition_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["health_conditions"]].insert_one(condition_dict)
        condition_dict["_id"] = str(result.inserted_id)
        return condition_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/health-conditions/{condition_id}")
def update_health_condition(condition_id: str, condition: mongo_models.HealthCondition):
    try:
        db = get_mongo_db()
        condition_dict = condition.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        condition_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["health_conditions"]].update_one(
            {"_id": ObjectId(condition_id)},
            {"$set": condition_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Health condition not found")
        
        updated_condition = db[COLLECTIONS["health_conditions"]].find_one({"_id": ObjectId(condition_id)})
        updated_condition["_id"] = str(updated_condition["_id"])
        return updated_condition
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/health-conditions/{condition_id}")
def delete_health_condition(condition_id: str):
    try:
        db = get_mongo_db()
        result = db[COLLECTIONS["health_conditions"]].delete_one({"_id": ObjectId(condition_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Health condition not found")
        return {"message": "Health condition deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== LIFESTYLE FACTOR ENDPOINTS ====================

@router.get("/lifestyle-factors/",
    summary="Get all lifestyle factors",
    description="Retrieve all lifestyle factor records with optional pagination"
)
def get_all_lifestyle_factors(skip: int = 0, limit: int = 100):
    try:
        db = get_mongo_db()
        lifestyle_factors = list(db[COLLECTIONS["lifestyle_factors"]].find().skip(skip).limit(limit))
        
        for lifestyle in lifestyle_factors:
            lifestyle["_id"] = str(lifestyle["_id"])
        
        return {
            "total": db[COLLECTIONS["lifestyle_factors"]].count_documents({}),
            "skip": skip,
            "limit": limit,
            "lifestyle_factors": lifestyle_factors
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/latest",
    summary="Get latest lifestyle factors",
    description="Retrieve the most recently created or updated lifestyle factor records"
)
def get_latest_lifestyle_factors(limit: int = 10):
    try:
        db = get_mongo_db()
        lifestyle_factors = list(
            db[COLLECTIONS["lifestyle_factors"]]
            .find()
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        for lifestyle in lifestyle_factors:
            lifestyle["_id"] = str(lifestyle["_id"])
        
        return {
            "limit": limit,
            "count": len(lifestyle_factors),
            "lifestyle_factors": lifestyle_factors
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/patient/{patient_id}",
    summary="Get lifestyle factors by PatientID",
    description="Retrieve all lifestyle factors for a specific patient"
)
def get_lifestyle_factors_by_patient(patient_id: int):
    try:
        db = get_mongo_db()
        lifestyle_factors = list(db[COLLECTIONS["lifestyle_factors"]].find({"PatientID": patient_id}))
        
        for lifestyle in lifestyle_factors:
            lifestyle["_id"] = str(lifestyle["_id"])
        
        return {
            "PatientID": patient_id,
            "total": len(lifestyle_factors),
            "lifestyle_factors": lifestyle_factors
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/{lifestyle_id}",
    summary="Get lifestyle factor by ID",
    description="Retrieve a single lifestyle factor record by ID"
)
def get_lifestyle_factor_by_id(lifestyle_id: str):
    try:
        db = get_mongo_db()
        lifestyle = db[COLLECTIONS["lifestyle_factors"]].find_one({"_id": ObjectId(lifestyle_id)})
        
        if not lifestyle:
            raise HTTPException(status_code=404, detail="Lifestyle factor not found")
        
        lifestyle["_id"] = str(lifestyle["_id"])
        return lifestyle
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/lifestyle-factors/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lifestyle factor",
    description="Create a new lifestyle factor record in MongoDB"
)
def create_lifestyle_factor(lifestyle: mongo_models.LifestyleFactor):
    try:
        db = get_mongo_db()
        lifestyle_dict = lifestyle.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        lifestyle_dict["created_at"] = datetime.utcnow()
        lifestyle_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["lifestyle_factors"]].insert_one(lifestyle_dict)
        lifestyle_dict["_id"] = str(result.inserted_id)
        return lifestyle_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/lifestyle-factors/{lifestyle_id}")
def update_lifestyle_factor(lifestyle_id: str, lifestyle: mongo_models.LifestyleFactor):
    try:
        db = get_mongo_db()
        lifestyle_dict = lifestyle.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        lifestyle_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["lifestyle_factors"]].update_one(
            {"_id": ObjectId(lifestyle_id)},
            {"$set": lifestyle_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lifestyle factor not found")
        
        updated_lifestyle = db[COLLECTIONS["lifestyle_factors"]].find_one({"_id": ObjectId(lifestyle_id)})
        updated_lifestyle["_id"] = str(updated_lifestyle["_id"])
        return updated_lifestyle
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/lifestyle-factors/{lifestyle_id}")
def delete_lifestyle_factor(lifestyle_id: str):
    try:
        db = get_mongo_db()
        result = db[COLLECTIONS["lifestyle_factors"]].delete_one({"_id": ObjectId(lifestyle_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Lifestyle factor not found")
        return {"message": "Lifestyle factor deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== HEALTH METRIC ENDPOINTS ====================

@router.get("/health-metrics/",
    summary="Get all health metrics",
    description="Retrieve all health metric records with optional pagination"
)
def get_all_health_metrics(skip: int = 0, limit: int = 100):
    try:
        db = get_mongo_db()
        metrics = list(db[COLLECTIONS["health_metrics"]].find().skip(skip).limit(limit))
        
        for metric in metrics:
            metric["_id"] = str(metric["_id"])
        
        return {
            "total": db[COLLECTIONS["health_metrics"]].count_documents({}),
            "skip": skip,
            "limit": limit,
            "health_metrics": metrics
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-metrics/latest",
    summary="Get latest health metrics",
    description="Retrieve the most recently created or updated health metric records"
)
def get_latest_health_metrics(limit: int = 10):
    try:
        db = get_mongo_db()
        metrics = list(
            db[COLLECTIONS["health_metrics"]]
            .find()
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        for metric in metrics:
            metric["_id"] = str(metric["_id"])
        
        return {
            "limit": limit,
            "count": len(metrics),
            "health_metrics": metrics
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-metrics/patient/{patient_id}",
    summary="Get health metrics by PatientID",
    description="Retrieve all health metrics for a specific patient"
)
def get_health_metrics_by_patient(patient_id: int):
    try:
        db = get_mongo_db()
        metrics = list(db[COLLECTIONS["health_metrics"]].find({"PatientID": patient_id}))
        
        for metric in metrics:
            metric["_id"] = str(metric["_id"])
        
        return {
            "PatientID": patient_id,
            "total": len(metrics),
            "health_metrics": metrics
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health-metrics/{metric_id}",
    summary="Get health metric by ID",
    description="Retrieve a single health metric record by ID"
)
def get_health_metric_by_id(metric_id: str):
    try:
        db = get_mongo_db()
        metric = db[COLLECTIONS["health_metrics"]].find_one({"_id": ObjectId(metric_id)})
        
        if not metric:
            raise HTTPException(status_code=404, detail="Health metric not found")
        
        metric["_id"] = str(metric["_id"])
        return metric
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/health-metrics/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health metric",
    description="Create a new health metric record in MongoDB"
)
def create_health_metric(metric: mongo_models.HealthMetric):
    try:
        db = get_mongo_db()
        metric_dict = metric.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        metric_dict["created_at"] = datetime.utcnow()
        metric_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["health_metrics"]].insert_one(metric_dict)
        metric_dict["_id"] = str(result.inserted_id)
        return metric_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/health-metrics/{metric_id}")
def update_health_metric(metric_id: str, metric: mongo_models.HealthMetric):
    try:
        db = get_mongo_db()
        metric_dict = metric.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        metric_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["health_metrics"]].update_one(
            {"_id": ObjectId(metric_id)},
            {"$set": metric_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Health metric not found")
        
        updated_metric = db[COLLECTIONS["health_metrics"]].find_one({"_id": ObjectId(metric_id)})
        updated_metric["_id"] = str(updated_metric["_id"])
        return updated_metric
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/health-metrics/{metric_id}")
def delete_health_metric(metric_id: str):
    try:
        db = get_mongo_db()
        result = db[COLLECTIONS["health_metrics"]].delete_one({"_id": ObjectId(metric_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Health metric not found")
        return {"message": "Health metric deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== HEALTHCARE ACCESS ENDPOINTS ====================

@router.get("/healthcare-access/",
    summary="Get all healthcare access records",
    description="Retrieve all healthcare access records with optional pagination"
)
def get_all_healthcare_access(skip: int = 0, limit: int = 100):
    try:
        db = get_mongo_db()
        access_records = list(db[COLLECTIONS["healthcare_access"]].find().skip(skip).limit(limit))
        
        for access in access_records:
            access["_id"] = str(access["_id"])
        
        return {
            "total": db[COLLECTIONS["healthcare_access"]].count_documents({}),
            "skip": skip,
            "limit": limit,
            "healthcare_access": access_records
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/healthcare-access/latest",
    summary="Get latest healthcare access records",
    description="Retrieve the most recently created or updated healthcare access records"
)
def get_latest_healthcare_access(limit: int = 10):
    try:
        db = get_mongo_db()
        access_records = list(
            db[COLLECTIONS["healthcare_access"]]
            .find()
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        for access in access_records:
            access["_id"] = str(access["_id"])
        
        return {
            "limit": limit,
            "count": len(access_records),
            "healthcare_access": access_records
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/healthcare-access/patient/{patient_id}",
    summary="Get healthcare access by PatientID",
    description="Retrieve all healthcare access records for a specific patient"
)
def get_healthcare_access_by_patient(patient_id: int):
    try:
        db = get_mongo_db()
        access_records = list(db[COLLECTIONS["healthcare_access"]].find({"PatientID": patient_id}))
        
        for access in access_records:
            access["_id"] = str(access["_id"])
        
        return {
            "PatientID": patient_id,
            "total": len(access_records),
            "healthcare_access": access_records
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/healthcare-access/{access_id}",
    summary="Get healthcare access by ID",
    description="Retrieve a single healthcare access record by ID"
)
def get_healthcare_access_by_id(access_id: str):
    try:
        db = get_mongo_db()
        access = db[COLLECTIONS["healthcare_access"]].find_one({"_id": ObjectId(access_id)})
        
        if not access:
            raise HTTPException(status_code=404, detail="Healthcare access record not found")
        
        access["_id"] = str(access["_id"])
        return access
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/healthcare-access/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new healthcare access record",
    description="Create a new healthcare access record in MongoDB"
)
def create_healthcare_access(access: mongo_models.HealthcareAccess):
    try:
        db = get_mongo_db()
        access_dict = access.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        access_dict["created_at"] = datetime.utcnow()
        access_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["healthcare_access"]].insert_one(access_dict)
        access_dict["_id"] = str(result.inserted_id)
        return access_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/healthcare-access/{access_id}")
def update_healthcare_access(access_id: str, access: mongo_models.HealthcareAccess):
    try:
        db = get_mongo_db()
        access_dict = access.dict(exclude_unset=True, by_alias=True, exclude={"id"})
        access_dict["updated_at"] = datetime.utcnow()
        
        result = db[COLLECTIONS["healthcare_access"]].update_one(
            {"_id": ObjectId(access_id)},
            {"$set": access_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Healthcare access record not found")
        
        updated_access = db[COLLECTIONS["healthcare_access"]].find_one({"_id": ObjectId(access_id)})
        updated_access["_id"] = str(updated_access["_id"])
        return updated_access
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/healthcare-access/{access_id}")
def delete_healthcare_access(access_id: str):
    try:
        db = get_mongo_db()
        result = db[COLLECTIONS["healthcare_access"]].delete_one({"_id": ObjectId(access_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Healthcare access record not found")
        return {"message": "Healthcare access record deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==================== AGGREGATED LATEST RECORDS ENDPOINT ====================

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