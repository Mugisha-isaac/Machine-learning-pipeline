from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.models.mongo_models import MongoPatient, MongoHealthCondition, MongoLifestyleFactor, MongoHealthMetric, MongoHealthcareAccess
from app.core.config import COLLECTIONS

router = APIRouter(prefix="/mongo", tags=["mongodb"])

# Patient routes
@router.post("/patients/", response_model=MongoPatient)
async def create_mongo_patient(patient: MongoPatient):
    db = get_mongo_db()
    patient_dict = patient.dict(by_alias=True)
    patient_dict["created_at"] = datetime.utcnow()
    patient_dict["updated_at"] = datetime.utcnow()
    
    result = db[COLLECTIONS["patients"]].insert_one(patient_dict)
    patient_dict["_id"] = result.inserted_id
    return MongoPatient(**patient_dict)

@router.put("/patients/{patient_id}", response_model=MongoPatient)
async def update_mongo_patient(patient_id: str, patient: MongoPatient):
    db = get_mongo_db()
    patient_dict = patient.dict(by_alias=True, exclude={'_id'})
    patient_dict["updated_at"] = datetime.utcnow()
    
    result = db[COLLECTIONS["patients"]].update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": patient_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    updated_patient = db[COLLECTIONS["patients"]].find_one({"_id": ObjectId(patient_id)})
    return MongoPatient(**updated_patient)

@router.delete("/patients/{patient_id}")
async def delete_mongo_patient(patient_id: str):
    db = get_mongo_db()
    result = db[COLLECTIONS["patients"]].delete_one({"_id": ObjectId(patient_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# Health Condition routes
@router.post("/health-conditions/", response_model=MongoHealthCondition)
async def create_mongo_health_condition(condition: MongoHealthCondition):
    db = get_mongo_db()
    condition_dict = condition.dict(by_alias=True)
    condition_dict["created_at"] = datetime.utcnow()
    condition_dict["updated_at"] = datetime.utcnow()
    
    result = db[COLLECTIONS["health_conditions"]].insert_one(condition_dict)
    condition_dict["_id"] = result.inserted_id
    return MongoHealthCondition(**condition_dict)

@router.put("/health-conditions/{condition_id}", response_model=MongoHealthCondition)
async def update_mongo_health_condition(condition_id: str, condition: MongoHealthCondition):
    db = get_mongo_db()
    condition_dict = condition.dict(by_alias=True, exclude={'_id'})
    condition_dict["updated_at"] = datetime.utcnow()
    
    result = db[COLLECTIONS["health_conditions"]].update_one(
        {"_id": ObjectId(condition_id)},
        {"$set": condition_dict}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Health condition not found")
    
    updated_condition = db[COLLECTIONS["health_conditions"]].find_one({"_id": ObjectId(condition_id)})
    return MongoHealthCondition(**updated_condition)

@router.delete("/health-conditions/{condition_id}")
async def delete_mongo_health_condition(condition_id: str):
    db = get_mongo_db()
    result = db[COLLECTIONS["health_conditions"]].delete_one({"_id": ObjectId(condition_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Health condition not found")
    return {"message": "Health condition deleted successfully"}