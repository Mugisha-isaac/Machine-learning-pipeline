from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import math

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import PatientCreate, PatientResponse, PatientsListResponse

router = APIRouter(tags=["PostgreSQL - Patients"])


@router.get("/",
    response_model=PatientsListResponse,
    summary="Get all patients with pagination",
    description="Retrieve patient records with pagination support. Returns items, total count, page number, and total pages."
)
def get_all_patients(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page (max 1000)"),
    db: Session = Depends(get_postgres_session)
):
    """
    Get paginated list of patients.
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 100, max: 1000)
    - Returns: List of patients with pagination metadata
    """
    try:
        # Get total count
        total = db.query(func.count(models.Patient.PatientID)).scalar()
        
        # Calculate offset and total pages
        skip = (page - 1) * page_size
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        # Get paginated results
        patients = db.query(models.Patient).offset(skip).limit(page_size).all()
        
        return {
            "items": patients,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/latest",
    response_model=List[PatientResponse],
    summary="Get latest patients",
    description="Retrieve the most recently created patient records"
)
def get_latest_patients(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        patients = db.query(models.Patient).order_by(models.Patient.PatientID.desc()).limit(limit).all()
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{patient_id}",
    response_model=PatientResponse,
    summary="Get patient by ID",
    description="Retrieve a single patient record by ID"
)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient",
    description="Create a new patient record in PostgreSQL"
)
def create_patient(patient: PatientCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_patient = models.Patient(**patient.dict())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for field, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
