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

@router.get("/patients/",
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


@router.get("/patients/latest",
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


@router.get("/patients/{patient_id}",
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

@router.get("/health-conditions/",
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


@router.get("/health-conditions/latest",
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


@router.get("/health-conditions/patient/{patient_id}",
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


@router.get("/health-conditions/{condition_id}",
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

@router.get("/lifestyle-factors/",
    response_model=List[LifestyleFactorResponse],
    summary="Get all lifestyle factors",
    description="Retrieve all lifestyle factor records with optional pagination"
)
def get_all_lifestyle_factors(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).offset(skip).limit(limit).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/latest",
    response_model=List[LifestyleFactorResponse],
    summary="Get latest lifestyle factors",
    description="Retrieve the most recently created lifestyle factor records"
)
def get_latest_lifestyle_factors(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).order_by(models.LifestyleFactor.LifestyleID.desc()).limit(limit).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/patient/{patient_id}",
    response_model=List[LifestyleFactorResponse],
    summary="Get lifestyle factors by PatientID",
    description="Retrieve all lifestyle factors for a specific patient"
)
def get_lifestyle_factors_by_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.PatientID == patient_id).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/lifestyle-factors/{lifestyle_id}",
    response_model=LifestyleFactorResponse,
    summary="Get lifestyle factor by ID",
    description="Retrieve a single lifestyle factor record by ID"
)
def get_lifestyle_factor_by_id(lifestyle_id: int, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
        if not lifestyle:
            raise HTTPException(status_code=404, detail="Lifestyle factor not found")
        return lifestyle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


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

@router.get("/health-metrics/",
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


@router.get("/health-metrics/latest",
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


@router.get("/health-metrics/patient/{patient_id}",
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


@router.get("/health-metrics/{metric_id}",
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

@router.get("/healthcare-access/",
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


@router.get("/healthcare-access/latest",
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


@router.get("/healthcare-access/patient/{patient_id}",
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


@router.get("/healthcare-access/{access_id}",
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

# ==================== MODEL TRAINING DATA ENDPOINTS ====================

@router.get("/training-data/latest",
    summary="Get latest complete patient records for model training",
    description="Retrieve latest patient records with all related health data (conditions, lifestyle, metrics, access)"
)
def get_latest_training_data(limit: int = 100, db: Session = Depends(get_postgres_session)):
    """
    Get the most recent patient records with all related information for ML model training.
    Returns complete dataset including demographics, health conditions, lifestyle factors,
    health metrics, and healthcare access information.
    """
    try:
        # Get latest patients
        patients = db.query(models.Patient).order_by(models.Patient.PatientID.desc()).limit(limit).all()
        
        training_data = []
        for patient in patients:
            # Get related data for each patient
            health_conditions = db.query(models.HealthCondition).filter(
                models.HealthCondition.PatientID == patient.PatientID
            ).first()
            
            lifestyle_factors = db.query(models.LifestyleFactor).filter(
                models.LifestyleFactor.PatientID == patient.PatientID
            ).first()
            
            health_metrics = db.query(models.HealthMetric).filter(
                models.HealthMetric.PatientID == patient.PatientID
            ).first()
            
            healthcare_access = db.query(models.HealthcareAccess).filter(
                models.HealthcareAccess.PatientID == patient.PatientID
            ).first()
            
            # Combine all data into a single record
            record = {
                "PatientID": patient.PatientID,
                "Sex": patient.Sex,
                "Age": patient.Age,
                "Education": patient.Education,
                "Income": patient.Income,
                # Health Conditions
                "Diabetes_012": health_conditions.Diabetes_012 if health_conditions else None,
                "HighBP": health_conditions.HighBP if health_conditions else None,
                "HighChol": health_conditions.HighChol if health_conditions else None,
                "Stroke": health_conditions.Stroke if health_conditions else None,
                "HeartDiseaseorAttack": health_conditions.HeartDiseaseorAttack if health_conditions else None,
                "DiffWalk": health_conditions.DiffWalk if health_conditions else None,
                # Lifestyle Factors
                "BMI": lifestyle_factors.BMI if lifestyle_factors else None,
                "Smoker": lifestyle_factors.Smoker if lifestyle_factors else None,
                "PhysActivity": lifestyle_factors.PhysActivity if lifestyle_factors else None,
                "Fruits": lifestyle_factors.Fruits if lifestyle_factors else None,
                "Veggies": lifestyle_factors.Veggies if lifestyle_factors else None,
                "HvyAlcoholConsump": lifestyle_factors.HvyAlcoholConsump if lifestyle_factors else None,
                # Health Metrics
                "CholCheck": health_metrics.CholCheck if health_metrics else None,
                "GenHlth": health_metrics.GenHlth if health_metrics else None,
                "MentHlth": health_metrics.MentHlth if health_metrics else None,
                "PhysHlth": health_metrics.PhysHlth if health_metrics else None,
                # Healthcare Access
                "AnyHealthcare": healthcare_access.AnyHealthcare if healthcare_access else None,
                "NoDocbcCost": healthcare_access.NoDocbcCost if healthcare_access else None,
            }
            training_data.append(record)
        
        return {
            "total": len(training_data),
            "limit": limit,
            "records": training_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/training-data/complete",
    summary="Get all complete patient records for model training",
    description="Retrieve all patient records that have complete data across all tables"
)
def get_complete_training_data(skip: int = 0, limit: int = 1000, db: Session = Depends(get_postgres_session)):
    """
    Get patient records with complete data (no null values) for ML model training.
    Only returns patients who have entries in all related tables.
    """
    try:
        # Query patients with all related data using joins
        query = db.query(
            models.Patient,
            models.HealthCondition,
            models.LifestyleFactor,
            models.HealthMetric,
            models.HealthcareAccess
        ).join(
            models.HealthCondition,
            models.Patient.PatientID == models.HealthCondition.PatientID
        ).join(
            models.LifestyleFactor,
            models.Patient.PatientID == models.LifestyleFactor.PatientID
        ).join(
            models.HealthMetric,
            models.Patient.PatientID == models.HealthMetric.PatientID
        ).join(
            models.HealthcareAccess,
            models.Patient.PatientID == models.HealthcareAccess.PatientID
        ).order_by(models.Patient.PatientID.desc()).offset(skip).limit(limit)
        
        results = query.all()
        
        training_data = []
        for patient, condition, lifestyle, metric, access in results:
            record = {
                "PatientID": patient.PatientID,
                "Sex": patient.Sex,
                "Age": patient.Age,
                "Education": patient.Education,
                "Income": patient.Income,
                # Health Conditions
                "Diabetes_012": condition.Diabetes_012,
                "HighBP": condition.HighBP,
                "HighChol": condition.HighChol,
                "Stroke": condition.Stroke,
                "HeartDiseaseorAttack": condition.HeartDiseaseorAttack,
                "DiffWalk": condition.DiffWalk,
                # Lifestyle Factors
                "BMI": lifestyle.BMI,
                "Smoker": lifestyle.Smoker,
                "PhysActivity": lifestyle.PhysActivity,
                "Fruits": lifestyle.Fruits,
                "Veggies": lifestyle.Veggies,
                "HvyAlcoholConsump": lifestyle.HvyAlcoholConsump,
                # Health Metrics
                "CholCheck": metric.CholCheck,
                "GenHlth": metric.GenHlth,
                "MentHlth": metric.MentHlth,
                "PhysHlth": metric.PhysHlth,
                # Healthcare Access
                "AnyHealthcare": access.AnyHealthcare,
                "NoDocbcCost": access.NoDocbcCost,
            }
            training_data.append(record)
        
        # Get total count of complete records
        total_count = db.query(models.Patient).join(
            models.HealthCondition
        ).join(
            models.LifestyleFactor
        ).join(
            models.HealthMetric
        ).join(
            models.HealthcareAccess
        ).count()
        
        return {
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "returned": len(training_data),
            "records": training_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )