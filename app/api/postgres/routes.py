from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.core.database import get_postgres_session
from app.core import models

router = APIRouter(
    prefix="/postgres",
    tags=["PostgreSQL Operations"],
    responses={404: {"description": "Not found"}},
)

# Pydantic schemas for request/response
class PatientCreate(BaseModel):
    Sex: Optional[bool] = None
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None

class PatientResponse(BaseModel):
    PatientID: int
    Sex: Optional[bool] = None
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class HealthConditionCreate(BaseModel):
    PatientID: int
    Diabetes_012: Optional[bool] = None
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None

class HealthConditionResponse(BaseModel):
    ConditionID: int
    PatientID: int
    Diabetes_012: Optional[bool] = None
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)
        

class LifestyleFactorCreate(BaseModel):
    PatientID: int
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None

class LifestyleFactorResponse(BaseModel):
    LifestyleID: int
    PatientID: int
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)
        

class HealthMetricCreate(BaseModel):
    PatientID: int
    CholCheck: Optional[bool] = None
    GenHlth: Optional[int] = None
    MentHlth: Optional[int] = None
    PhysHlth: Optional[int] = None

class HealthMetricResponse(BaseModel):
    MetricsID: int
    PatientID: int
    CholCheck: Optional[bool] = None
    GenHlth: Optional[int] = None
    MentHlth: Optional[int] = None
    PhysHlth: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
        

class HealthcareAccessCreate(BaseModel):
    PatientID: int
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = None

class HealthcareAccessResponse(BaseModel):
    AccessID: int
    PatientID: int
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)
        

# ==================== PATIENT ENDPOINTS ====================

@router.post("/patients/",
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


@router.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for field, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    db_patient = db.query(models.Patient).filter(models.Patient.PatientID == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

# ==================== HEALTH CONDITION ENDPOINTS ====================

@router.post("/health-conditions/",
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


@router.put("/health-conditions/{condition_id}", response_model=HealthConditionResponse)
def update_health_condition(condition_id: int, condition: HealthConditionCreate, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(models.HealthCondition).filter(models.HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    
    for field, value in condition.dict(exclude_unset=True).items():
        setattr(db_condition, field, value)
    db.commit()
    db.refresh(db_condition)
    return db_condition

@router.delete("/health-conditions/{condition_id}")
def delete_health_condition(condition_id: int, db: Session = Depends(get_postgres_session)):
    db_condition = db.query(models.HealthCondition).filter(models.HealthCondition.ConditionID == condition_id).first()
    if not db_condition:
        raise HTTPException(status_code=404, detail="Health condition not found")
    db.delete(db_condition)
    db.commit()
    return {"message": "Health condition deleted successfully"}

# ==================== LIFESTYLE FACTOR ENDPOINTS ====================

@router.post("/lifestyle-factors/",
    response_model=LifestyleFactorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lifestyle factor",
    description="Create a new lifestyle factor record in PostgreSQL"
)
def create_lifestyle_factor(lifestyle: LifestyleFactorCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_lifestyle = models.LifestyleFactor(**lifestyle.dict())
        db.add(db_lifestyle)
        db.commit()
        db.refresh(db_lifestyle)
        return db_lifestyle
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/lifestyle-factors/{lifestyle_id}", response_model=LifestyleFactorResponse)
def update_lifestyle_factor(lifestyle_id: int, lifestyle: LifestyleFactorCreate, db: Session = Depends(get_postgres_session)):
    db_lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
    if not db_lifestyle:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    for field, value in lifestyle.dict(exclude_unset=True).items():
        setattr(db_lifestyle, field, value)
    db.commit()
    db.refresh(db_lifestyle)
    return db_lifestyle

@router.delete("/lifestyle-factors/{lifestyle_id}")
def delete_lifestyle_factor(lifestyle_id: int, db: Session = Depends(get_postgres_session)):
    db_lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
    if not db_lifestyle:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    db.delete(db_lifestyle)
    db.commit()
    return {"message": "Lifestyle factor deleted successfully"}

# ==================== HEALTH METRIC ENDPOINTS ====================

@router.post("/health-metrics/",
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


@router.put("/health-metrics/{metric_id}", response_model=HealthMetricResponse)
def update_health_metric(metric_id: int, metric: HealthMetricCreate, db: Session = Depends(get_postgres_session)):
    db_metric = db.query(models.HealthMetric).filter(models.HealthMetric.MetricsID == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    
    for field, value in metric.dict(exclude_unset=True).items():
        setattr(db_metric, field, value)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.delete("/health-metrics/{metric_id}")
def delete_health_metric(metric_id: int, db: Session = Depends(get_postgres_session)):
    db_metric = db.query(models.HealthMetric).filter(models.HealthMetric.MetricsID == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    db.delete(db_metric)
    db.commit()
    return {"message": "Health metric deleted successfully"}

# ==================== HEALTHCARE ACCESS ENDPOINTS ====================

@router.post("/healthcare-access/",
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


@router.put("/healthcare-access/{access_id}", response_model=HealthcareAccessResponse)
def update_healthcare_access(access_id: int, access: HealthcareAccessCreate, db: Session = Depends(get_postgres_session)):
    db_access = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.AccessID == access_id).first()
    if not db_access:
        raise HTTPException(status_code=404, detail="Healthcare access record not found")
    
    for field, value in access.dict(exclude_unset=True).items():
        setattr(db_access, field, value)
    db.commit()
    db.refresh(db_access)
    return db_access

@router.delete("/healthcare-access/{access_id}")
def delete_healthcare_access(access_id: int, db: Session = Depends(get_postgres_session)):
    db_access = db.query(models.HealthcareAccess).filter(models.HealthcareAccess.AccessID == access_id).first()
    if not db_access:
        raise HTTPException(status_code=404, detail="Healthcare access record not found")
    db.delete(db_access)
    db.commit()
    return {"message": "Healthcare access record deleted successfully"}