"""
MongoDB Health Conditions Controller
Handles all health condition-related operations for MongoDB
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(tags=["MongoDB - Health Conditions"])


@router.get("/",
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


@router.get("/latest",
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


@router.get("/patient/{patient_id}",
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


@router.get("/{condition_id}",
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


@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health condition",
    description="Create a new health condition record in MongoDB (no need to send _id)"
)
def create_health_condition(condition: mongo_models.HealthConditionCreate):
    try:
        db = get_mongo_db()
        condition_dict = condition.model_dump(exclude_unset=True)
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


@router.put("/{condition_id}",
    summary="Update health condition",
    description="Update health condition record in MongoDB (no need to send _id)"
)
def update_health_condition(condition_id: str, condition: mongo_models.HealthConditionUpdate):
    try:
        db = get_mongo_db()
        condition_dict = condition.model_dump(exclude_unset=True)
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


@router.delete("/{condition_id}")
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
