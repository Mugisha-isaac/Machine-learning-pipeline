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