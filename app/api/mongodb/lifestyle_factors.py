"""
MongoDB Lifestyle Factors Controller
Handles all lifestyle factor-related operations for MongoDB
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(tags=["MongoDB - Lifestyle Factors"])


@router.get("/",
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


@router.get("/latest",
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


@router.get("/patient/{patient_id}",
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


@router.get("/{lifestyle_id}",
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


@router.post("/", 
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


@router.put("/{lifestyle_id}")
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


@router.delete("/{lifestyle_id}")
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
