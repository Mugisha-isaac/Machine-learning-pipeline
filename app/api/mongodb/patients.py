"""
MongoDB Patients Controller
Handles all patient-related operations for MongoDB
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(tags=["MongoDB - Patients"])


@router.get("/",
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


@router.get("/latest",
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


@router.get("/by-patient-id/{patient_id}",
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


@router.get("/{patient_id}",
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


@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient",
    description="Create a new patient record in MongoDB (no need to send _id)"
)
def create_patient(patient: mongo_models.PatientCreate):
    try:
        db = get_mongo_db()
        patient_dict = patient.model_dump(exclude_unset=True)
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


@router.put("/{patient_id}",
    summary="Update patient",
    description="Update patient record in MongoDB (no need to send _id)"
)
def update_patient(patient_id: str, patient: mongo_models.PatientUpdate):
    try:
        db = get_mongo_db()
        patient_dict = patient.model_dump(exclude_unset=True)
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


@router.delete("/{patient_id}")
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
