from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import HealthMetricCreate, HealthMetricResponse

router = APIRouter(tags=["PostgreSQL - Health Metrics"])


@router.get("/",
    response_model=List[HealthMetricResponse],
    summary="Get all health metrics",
    description="Retrieve all health metric records with optional pagination"
)
def get_all_health_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        metrics = db.query(models.HealthMetric).offset(skip).limit(limit).all()
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/latest",
    response_model=List[HealthMetricResponse],
    summary="Get latest health metrics",
    description="Retrieve the most recently created health metric records"
)
def get_latest_health_metrics(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        metrics = db.query(models.HealthMetric).order_by(models.HealthMetric.MetricsID.desc()).limit(limit).all()
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patient/{patient_id}",
    response_model=List[HealthMetricResponse],
    summary="Get health metrics by PatientID",
    description="Retrieve all health metrics for a specific patient"
)
def get_health_metrics_by_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        metrics = db.query(models.HealthMetric).filter(models.HealthMetric.PatientID == patient_id).all()
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{metric_id}",
    response_model=HealthMetricResponse,
    summary="Get health metric by ID",
    description="Retrieve a single health metric record by ID"
)
def get_health_metric_by_id(metric_id: int, db: Session = Depends(get_postgres_session)):
    try:
        metric = db.query(models.HealthMetric).filter(models.HealthMetric.MetricsID == metric_id).first()
        if not metric:
            raise HTTPException(status_code=404, detail="Health metric not found")
        return metric
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/",
    response_model=HealthMetricResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health metric",
    description="Create a new health metric record in PostgreSQL"
)
def create_health_metric(metric: HealthMetricCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_metric = models.HealthMetric(**metric.dict())
        db.add(db_metric)
        db.commit()
        db.refresh(db_metric)
        return db_metric
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{metric_id}", response_model=HealthMetricResponse)
def update_health_metric(metric_id: int, metric: HealthMetricCreate, db: Session = Depends(get_postgres_session)):
    db_metric = db.query(models.HealthMetric).filter(models.HealthMetric.MetricsID == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    
    for field, value in metric.dict(exclude_unset=True).items():
        setattr(db_metric, field, value)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.delete("/{metric_id}")
def delete_health_metric(metric_id: int, db: Session = Depends(get_postgres_session)):
    db_metric = db.query(models.HealthMetric).filter(models.HealthMetric.MetricsID == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    db.delete(db_metric)
    db.commit()
    return {"message": "Health metric deleted successfully"}
