"""
MongoDB Healthcare Access Controller
Handles all healthcare access-related operations for MongoDB
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(tags=["MongoDB - Healthcare Access"])


@router.get("/",
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


@router.get("/latest",
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


@router.get("/patient/{patient_id}",
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


@router.get("/{access_id}",
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


@router.post("/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new healthcare access record",
    description="Create a new healthcare access record in MongoDB (no need to send _id)"
)
def create_healthcare_access(access: mongo_models.HealthcareAccessCreate):
    try:
        db = get_mongo_db()
        access_dict = access.model_dump(exclude_unset=True)
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


@router.put("/{access_id}",
    summary="Update healthcare access",
    description="Update healthcare access record in MongoDB (no need to send _id)"
)
def update_healthcare_access(access_id: str, access: mongo_models.HealthcareAccessUpdate):
    try:
        db = get_mongo_db()
        access_dict = access.model_dump(exclude_unset=True)
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


@router.delete("/{access_id}")
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
