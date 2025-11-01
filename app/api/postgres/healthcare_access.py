from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import HealthcareAccessCreate, HealthcareAccessResponse

router = APIRouter(tags=["PostgreSQL - Healthcare Access"])


@router.get("/",
    response_model=List[HealthcareAccessResponse],
    summary="Get all healthcare access records",
    description="Retrieve all healthcare access records with optional pagination"
)
def get_all_healthcare_access(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        access_records = db.query(models.HealthcareAccess).offset(skip).limit(limit).all()
        return access_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/latest",
    response_model=List[HealthcareAccessResponse],
    summary="Get latest healthcare access records",
    description="Retrieve the most recently created healthcare access records"
)
def get_latest_healthcare_access(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        access_records = db.query(models.HealthcareAccess).order_by(models.HealthcareAccess.AccessID.desc()).limit(limit).all()
        return access_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patient/{patient_id}",
    response_model=List[HealthcareAccessResponse],
    summary="Get healthcare access by PatientID",
    description="Retrieve all healthcare access records for a specific patient"
)
def get_healthcare_access_by_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        access_records = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.PatientID == patient_id).all()
        return access_records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{access_id}",
    response_model=HealthcareAccessResponse,
    summary="Get healthcare access by ID",
    description="Retrieve a single healthcare access record by ID"
)
def get_healthcare_access_by_id(access_id: int, db: Session = Depends(get_postgres_session)):
    try:
        access = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.AccessID == access_id).first()
        if not access:
            raise HTTPException(status_code=404, detail="Healthcare access record not found")
        return access
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/",
    response_model=HealthcareAccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new healthcare access record",
    description="Create a new healthcare access record in PostgreSQL"
)
def create_healthcare_access(access: HealthcareAccessCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_access = models.HealthcareAccess(**access.dict())
        db.add(db_access)
        db.commit()
        db.refresh(db_access)
        return db_access
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{access_id}", response_model=HealthcareAccessResponse)
def update_healthcare_access(access_id: int, access: HealthcareAccessCreate, db: Session = Depends(get_postgres_session)):
    db_access = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.AccessID == access_id).first()
    if not db_access:
        raise HTTPException(status_code=404, detail="Healthcare access record not found")
    
    for field, value in access.dict(exclude_unset=True).items():
        setattr(db_access, field, value)
    db.commit()
    db.refresh(db_access)
    return db_access


@router.delete("/{access_id}")
def delete_healthcare_access(access_id: int, db: Session = Depends(get_postgres_session)):
    db_access = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.AccessID == access_id).first()
    if not db_access:
        raise HTTPException(status_code=404, detail="Healthcare access record not found")
    db.delete(db_access)
    db.commit()
    return {"message": "Healthcare access record deleted successfully"}
