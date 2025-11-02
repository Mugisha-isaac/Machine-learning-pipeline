"""
MongoDB Health Metrics Controller
Handles all health metric-related operations for MongoDB
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId

from app.core.database import get_mongo_db
from app.core import mongo_models, COLLECTIONS

router = APIRouter(tags=["MongoDB - Health Metrics"])


@router.get("/",
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


@router.get("/latest",
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


@router.get("/patient/{patient_id}",
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


@router.get("/{metric_id}",
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


@router.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health metric",
    description="Create a new health metric record in MongoDB (no need to send _id)"
)
def create_health_metric(metric: mongo_models.HealthMetricCreate):
    try:
        db = get_mongo_db()
        metric_dict = metric.model_dump(exclude_unset=True)
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


@router.put("/{metric_id}",
    summary="Update health metric",
    description="Update health metric record in MongoDB (no need to send _id)"
)
def update_health_metric(metric_id: str, metric: mongo_models.HealthMetricUpdate):
    try:
        db = get_mongo_db()
        metric_dict = metric.model_dump(exclude_unset=True)
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


@router.delete("/{metric_id}")
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
