from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import HealthConditionCreate, HealthConditionResponse

router = APIRouter(tags=["PostgreSQL - Health Conditions"])


@router.get("/",
    response_model=List[HealthConditionResponse],
    summary="Get all health conditions",
    description="Retrieve all health condition records with optional pagination"
)
def get_all_health_conditions(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        conditions = db.query(models.HealthCondition).offset(skip).limit(limit).all()
        return conditions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/latest",
    response_model=List[HealthConditionResponse],
    summary="Get latest health conditions",
    description="Retrieve the most recently created health condition records"
)
def get_latest_health_conditions(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        conditions = db.query(models.HealthCondition).order_by(models.HealthCondition.ConditionID.desc()).limit(limit).all()
        return conditions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patient/{patient_id}",
    response_model=List[HealthConditionResponse],
    summary="Get health conditions by PatientID",
    description="Retrieve all health conditions for a specific patient"
)
def get_health_conditions_by_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        conditions = db.query(models.HealthCondition).filter(models.HealthCondition.PatientID == patient_id).all()
        return conditions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{condition_id}",
    response_model=HealthConditionResponse,
    summary="Get health condition by ID",
    description="Retrieve a single health condition record by ID"
)
def get_health_condition_by_id(condition_id: int, db: Session = Depends(get_postgres_session)):
    try:
        condition = db.query(models.HealthCondition).filter(models.HealthCondition.ConditionID == condition_id).first()
        if not condition:
            raise HTTPException(status_code=404, detail="Health condition not found")
        return condition
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/",
    response_model=HealthConditionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new health condition",
    description="Create a new health condition record in PostgreSQL"
)
def create_health_condition(condition: HealthConditionCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_condition = models.HealthCondition(**condition.dict())
        db.add(db_condition)
        db.commit()
        db.refresh(db_condition)
        return db_condition
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{condition_id}", response_model=HealthConditionResponse)
def update_health_condition(condition_id: int, condition: HealthConditionCreate, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(models.HealthCondition).filter(models.HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    
    for field, value in condition.dict(exclude_unset=True).items():
        setattr(db_condition, field, value)
    db.commit()
    db.refresh(db_condition)
    return db_condition


@router.delete("/{condition_id}")
def delete_health_condition(condition_id: int, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(models.HealthCondition).filter(models.HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    db.delete(db_condition)
    db.commit()
    return {"message": "Health condition deleted successfully"}
