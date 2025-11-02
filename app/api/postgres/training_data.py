from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_postgres_session
from app.core import models

router = APIRouter(tags=["PostgreSQL - Training Data"])


@router.get("/latest",
    summary="Get latest complete patient records for model training",
    description="Retrieve latest patient records with all related health data (conditions, lifestyle, metrics, access) using stored procedure"
)
def get_latest_training_data(limit: int = 100, db: Session = Depends(get_postgres_session)):
    """
    Get the most recent patient records with all related information for ML model training.
    Uses GetPatientProfile stored procedure for efficient data retrieval.
    Returns complete dataset including demographics, health conditions, lifestyle factors,
    health metrics, and healthcare access information.
    """
    try:
        # Get latest patient IDs first
        patients = db.query(models.Patient).order_by(models.Patient.PatientID.desc()).limit(limit).all()
        patient_ids = [p.PatientID for p in patients]
        
        if not patient_ids:
            return {
                "total": 0,
                "limit": limit,
                "records": []
            }
        
        training_data = []
        # Call stored procedure for each patient
        for patient_id in patient_ids:
            result = db.execute(
                text("SELECT * FROM GetPatientProfile(:patient_id)"),
                {"patient_id": patient_id}
            ).fetchone()
            
            if result:
                # Access columns by index
                record = {
                    "PatientID": result[0],
                    "Sex": result[1],
                    "Age": result[2],
                    "Education": result[3],
                    "Income": result[4],
                    # Health Conditions
                    "Diabetes_012": result[6],
                    "HighBP": result[7],
                    "HighChol": result[8],
                    "Stroke": result[9],
                    "HeartDiseaseorAttack": result[10],
                    "DiffWalk": result[11],
                    # Lifestyle Factors
                    "BMI": result[13],
                    "Smoker": result[14],
                    "PhysActivity": result[15],
                    "Fruits": result[16],
                    "Veggies": result[17],
                    "HvyAlcoholConsump": result[18],
                    # Health Metrics
                    "CholCheck": result[20],
                    "GenHlth": result[21],
                    "MentHlth": result[22],
                    "PhysHlth": result[23],
                    # Healthcare Access
                    "AnyHealthcare": result[25],
                    "NoDocbcCost": result[26],
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
            detail=f"Error retrieving training data: {str(e)}"
        )


@router.get("/complete",
    summary="Get all complete patient records for model training",
    description="Retrieve all patient records that have complete data across all tables using stored procedure"
)
def get_complete_training_data(skip: int = 0, limit: int = 1000, db: Session = Depends(get_postgres_session)):
    """
    Get patient records with complete data (no null values) for ML model training.
    Uses GetCompletePatientRecords stored procedure for efficient querying.
    Only returns patients who have entries in all related tables.
    """
    try:
        # Call stored procedure to get complete patient records
        results = db.execute(
            text("SELECT * FROM GetCompletePatientRecords(:skip_count, :limit_count)"),
            {"skip_count": skip, "limit_count": limit}
        ).fetchall()
        
        training_data = []
        for result in results:
            # Access columns by index
            record = {
                "PatientID": result[0],
                "Sex": result[1],
                "Age": result[2],
                "Education": result[3],
                "Income": result[4],
                # Health Conditions
                "Diabetes_012": result[5],
                "HighBP": result[6],
                "HighChol": result[7],
                "Stroke": result[8],
                "HeartDiseaseorAttack": result[9],
                "DiffWalk": result[10],
                # Lifestyle Factors
                "BMI": result[11],
                "Smoker": result[12],
                "PhysActivity": result[13],
                "Fruits": result[14],
                "Veggies": result[15],
                "HvyAlcoholConsump": result[16],
                # Health Metrics
                "CholCheck": result[17],
                "GenHlth": result[18],
                "MentHlth": result[19],
                "PhysHlth": result[20],
                # Healthcare Access
                "AnyHealthcare": result[21],
                "NoDocbcCost": result[22],
            }
            training_data.append(record)
        
        # Get total count using a simple query
        total_count_query = db.execute(
            text("""
                SELECT COUNT(*) FROM "Patients" p
                INNER JOIN "Health_Conditions" hc ON p."PatientID" = hc."PatientID"
                INNER JOIN "Lifestyle_Factors" lf ON p."PatientID" = lf."PatientID"
                INNER JOIN "Health_Metrics" hm ON p."PatientID" = hm."PatientID"
                INNER JOIN "Healthcare_Access" ha ON p."PatientID" = ha."PatientID"
            """)
        ).scalar()
        
        return {
            "total": total_count_query or 0,
            "skip": skip,
            "limit": limit,
            "returned": len(training_data),
            "records": training_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving complete training data: {str(e)}"
        )
