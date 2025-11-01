from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_postgres_session
from app.core import models

router = APIRouter(tags=["PostgreSQL - Training Data"])


@router.get("/latest",
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


@router.get("/complete",
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
