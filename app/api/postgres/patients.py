from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import PatientCreate, PatientResponse

router = APIRouter(tags=["PostgreSQL - Patients"])


@router.get("/",
    response_model=List[PatientResponse],
    summary="Get all patients",
    description="Retrieve all patient records with optional pagination"
)
def get_all_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        patients = db.query(models.Patient).offset(skip).limit(limit).all()
        return patients
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
