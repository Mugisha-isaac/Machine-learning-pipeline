from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_postgres_session
from app.models.postgres_models import Patient, HealthCondition, LifestyleFactor, HealthMetric, HealthcareAccess

router = APIRouter(prefix="/postgres", tags=["postgres"])

# Patient routes
@router.post("/patients/", response_model=Patient)
def create_patient(patient: Patient, db: Session = Depends(get_postgres_session)):
    db_patient = Patient(**patient.dict(exclude={'PatientID'}))
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient: Patient, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(Patient).filter(Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for field, value in patient.dict(exclude={'PatientID'}).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(Patient).filter(Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

# Health Condition routes
@router.post("/health-conditions/", response_model=HealthCondition)
def create_health_condition(condition: HealthCondition, db: Session = Depends(get_postgres_session)):
    db_condition = HealthCondition(**condition.dict(exclude={'ConditionID'}))
    db.add(db_condition)
    db.commit()
    db.refresh(db_condition)
    return db_condition

@router.put("/health-conditions/{condition_id}", response_model=HealthCondition)
def update_health_condition(condition_id: int, condition: HealthCondition, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(HealthCondition).filter(HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    
    for field, value in condition.dict(exclude={'ConditionID'}).items():
        setattr(db_condition, field, value)
    db.commit()
    db.refresh(db_condition)
    return db_condition

@router.delete("/health-conditions/{condition_id}")
def delete_health_condition(condition_id: int, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(HealthCondition).filter(HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    db.delete(db_condition)
    db.commit()
    return {"message": "Health condition deleted successfully"}