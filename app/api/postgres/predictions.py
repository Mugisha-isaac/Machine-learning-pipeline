"""
PostgreSQL Predictions Controller
Handles ML model predictions using stored procedures
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path
import json
import numpy as np

from app.core.database import get_postgres_session

# ML model imports
try:
    from tensorflow.keras.models import load_model
    import joblib
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

router = APIRouter(tags=["PostgreSQL - Predictions"])

# Model configuration
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "model_exp5.h5"
SCALER_PATH = BASE_DIR / "models" / "scaler.joblib"
MODEL_VERSION = "model_exp5"

# Feature order expected by the model (must match training)
FEATURE_ORDER = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
    "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits",
    "Veggies", "HvyAlcoholConsump", "AnyHealthcare",
    "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk",
    "Sex", "Age", "Education", "Income"
]

LABELS = {0: "No Diabetes", 1: "Prediabetes", 2: "Diabetes"}

# Global model and scaler (loaded once)
_model = None
_scaler = None


def load_ml_model():
    """Load the ML model and scaler (singleton pattern)."""
    global _model, _scaler
    
    if not MODELS_AVAILABLE:
        raise RuntimeError("TensorFlow/Keras not available. Install with: pip install tensorflow joblib")
    
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = load_model(str(MODEL_PATH), compile=False)
    
    if _scaler is None and SCALER_PATH.exists():
        try:
            _scaler = joblib.load(str(SCALER_PATH))
        except Exception:
            pass  # Scaler is optional
    
    return _model, _scaler


def normalize_value(v):
    """Normalize a value for model input."""
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if v is None:
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def build_feature_vector(record: dict) -> np.ndarray:
    """Build feature vector from patient record."""
    vec = [normalize_value(record.get(f)) for f in FEATURE_ORDER]
    return np.array(vec, dtype=np.float32).reshape(1, -1)


def interpret_prediction(value: float) -> tuple:
    """Interpret raw prediction value into class and label."""
    cls = int(np.clip(np.rint(value), 0, 2))
    label = LABELS.get(cls, f"Class {cls}")
    return cls, label


def log_prediction_to_db(
    db: Session,
    patient_id: int,
    raw_output: float,
    predicted_class: int,
    predicted_label: str,
    feature_data: dict,
    model_version: str = MODEL_VERSION
) -> int:
    """Log prediction results to the Predictions table."""
    try:
        feature_snapshot = json.dumps(feature_data)
        
        insert_query = text("""
            INSERT INTO "Predictions" 
            ("PatientID", "RawOutput", "PredictedClass", "PredictedLabel", 
             "ModelVersion", "PredictedAt", "FeatureSnapshot")
            VALUES (:patient_id, :raw_output, :predicted_class, :predicted_label, 
                    :model_version, :predicted_at, :feature_snapshot)
            RETURNING "PredictionID"
        """)
        
        result = db.execute(insert_query, {
            "patient_id": patient_id,
            "raw_output": raw_output,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "model_version": model_version,
            "predicted_at": datetime.utcnow(),
            "feature_snapshot": feature_snapshot
        })
        
        prediction_id = result.fetchone()[0]
        db.commit()
        
        return prediction_id
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to log prediction: {str(e)}")


@router.post("/predict/patient/{patient_id}",
    summary="Make prediction for specific patient",
    description="Fetch patient data using stored procedure and make diabetes prediction"
)
def predict_for_patient(
    patient_id: int,
    db: Session = Depends(get_postgres_session)
):
    """
    Make diabetes prediction for a specific patient.
    
    - Fetches complete patient data using GetPatientProfile stored procedure
    - Preprocesses features
    - Makes prediction using trained ML model
    - Logs prediction to database
    - Returns prediction results
    """
    try:
        # Load model
        model, scaler = load_ml_model()
        
        # Fetch patient data using stored procedure
        result = db.execute(
            text("SELECT * FROM GetPatientProfile(:patient_id)"),
            {"patient_id": patient_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Patient {patient_id} not found or incomplete data"
            )
        
        # Map result to dictionary
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
        
        # Build feature vector
        feature_vector = build_feature_vector(record)
        original_features = {name: val for name, val in zip(FEATURE_ORDER, feature_vector.flatten().tolist())}
        
        # Apply scaler if available
        if scaler:
            feature_vector = scaler.transform(feature_vector)
        
        # Make prediction
        pred = model.predict(feature_vector, verbose=0)
        raw_value = float(np.asarray(pred).reshape(-1)[0])
        predicted_class, predicted_label = interpret_prediction(raw_value)
        
        # Log prediction to database
        prediction_id = log_prediction_to_db(
            db=db,
            patient_id=patient_id,
            raw_output=raw_value,
            predicted_class=predicted_class,
            predicted_label=predicted_label,
            feature_data=original_features,
            model_version=MODEL_VERSION
        )
        
        return {
            "success": True,
            "prediction_id": prediction_id,
            "patient_id": patient_id,
            "prediction": {
                "raw_output": round(raw_value, 4),
                "predicted_class": predicted_class,
                "predicted_label": predicted_label,
                "confidence": round(abs(raw_value - predicted_class), 4)
            },
            "model_version": MODEL_VERSION,
            "predicted_at": datetime.utcnow().isoformat(),
            "features_used": original_features
        }
        
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/latest",
    summary="Make prediction for latest patient",
    description="Fetch latest patient data and make diabetes prediction"
)
def predict_for_latest_patient(
    db: Session = Depends(get_postgres_session)
):
    """
    Make diabetes prediction for the most recent patient in the database.
    
    - Fetches latest complete patient record using stored procedure
    - Preprocesses features
    - Makes prediction using trained ML model
    - Logs prediction to database
    - Returns prediction results
    """
    try:
        # Load model
        model, scaler = load_ml_model()
        
        # Fetch latest complete patient record using stored procedure
        result = db.execute(
            text("SELECT * FROM GetCompletePatientRecords(0, 1)")
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No complete patient records found in database"
            )
        
        # Map result to dictionary
        patient_id = result[0]
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
        
        # Build feature vector
        feature_vector = build_feature_vector(record)
        original_features = {name: val for name, val in zip(FEATURE_ORDER, feature_vector.flatten().tolist())}
        
        # Apply scaler if available
        if scaler:
            feature_vector = scaler.transform(feature_vector)
        
        # Make prediction
        pred = model.predict(feature_vector, verbose=0)
        raw_value = float(np.asarray(pred).reshape(-1)[0])
        predicted_class, predicted_label = interpret_prediction(raw_value)
        
        # Log prediction to database
        prediction_id = log_prediction_to_db(
            db=db,
            patient_id=patient_id,
            raw_output=raw_value,
            predicted_class=predicted_class,
            predicted_label=predicted_label,
            feature_data=original_features,
            model_version=MODEL_VERSION
        )
        
        return {
            "success": True,
            "prediction_id": prediction_id,
            "patient_id": patient_id,
            "prediction": {
                "raw_output": round(raw_value, 4),
                "predicted_class": predicted_class,
                "predicted_label": predicted_label,
                "confidence": round(abs(raw_value - predicted_class), 4)
            },
            "model_version": MODEL_VERSION,
            "predicted_at": datetime.utcnow().isoformat(),
            "features_used": original_features
        }
        
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/batch",
    summary="Make predictions for multiple patients",
    description="Batch prediction for multiple patients using stored procedure"
)
def predict_batch(
    patient_ids: List[int],
    db: Session = Depends(get_postgres_session)
):
    """
    Make diabetes predictions for multiple patients.
    
    - Accepts list of patient IDs
    - Fetches data using stored procedure for each patient
    - Makes predictions in batch
    - Logs all predictions to database
    - Returns list of prediction results
    """
    if not patient_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient_ids list cannot be empty"
        )
    
    if len(patient_ids) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 patients per batch request"
        )
    
    try:
        # Load model
        model, scaler = load_ml_model()
        
        results = []
        
        for patient_id in patient_ids:
            try:
                # Fetch patient data using stored procedure
                result = db.execute(
                    text("SELECT * FROM GetPatientProfile(:patient_id)"),
                    {"patient_id": patient_id}
                ).fetchone()
                
                if not result:
                    results.append({
                        "patient_id": patient_id,
                        "success": False,
                        "error": "Patient not found or incomplete data"
                    })
                    continue
                
                # Map result to dictionary
                record = {
                    "PatientID": result[0],
                    "Sex": result[1],
                    "Age": result[2],
                    "Education": result[3],
                    "Income": result[4],
                    "Diabetes_012": result[6],
                    "HighBP": result[7],
                    "HighChol": result[8],
                    "Stroke": result[9],
                    "HeartDiseaseorAttack": result[10],
                    "DiffWalk": result[11],
                    "BMI": result[13],
                    "Smoker": result[14],
                    "PhysActivity": result[15],
                    "Fruits": result[16],
                    "Veggies": result[17],
                    "HvyAlcoholConsump": result[18],
                    "CholCheck": result[20],
                    "GenHlth": result[21],
                    "MentHlth": result[22],
                    "PhysHlth": result[23],
                    "AnyHealthcare": result[25],
                    "NoDocbcCost": result[26],
                }
                
                # Build feature vector
                feature_vector = build_feature_vector(record)
                original_features = {name: val for name, val in zip(FEATURE_ORDER, feature_vector.flatten().tolist())}
                
                # Apply scaler if available
                if scaler:
                    feature_vector = scaler.transform(feature_vector)
                
                # Make prediction
                pred = model.predict(feature_vector, verbose=0)
                raw_value = float(np.asarray(pred).reshape(-1)[0])
                predicted_class, predicted_label = interpret_prediction(raw_value)
                
                # Log prediction to database
                prediction_id = log_prediction_to_db(
                    db=db,
                    patient_id=patient_id,
                    raw_output=raw_value,
                    predicted_class=predicted_class,
                    predicted_label=predicted_label,
                    feature_data=original_features,
                    model_version=MODEL_VERSION
                )
                
                results.append({
                    "success": True,
                    "prediction_id": prediction_id,
                    "patient_id": patient_id,
                    "prediction": {
                        "raw_output": round(raw_value, 4),
                        "predicted_class": predicted_class,
                        "predicted_label": predicted_label
                    }
                })
                
            except Exception as e:
                results.append({
                    "patient_id": patient_id,
                    "success": False,
                    "error": str(e)
                })
        
        successful = sum(1 for r in results if r.get("success"))
        
        return {
            "total_requested": len(patient_ids),
            "successful_predictions": successful,
            "failed_predictions": len(patient_ids) - successful,
            "model_version": MODEL_VERSION,
            "results": results
        }
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.get("/predictions/",
    summary="Get all predictions",
    description="Retrieve all prediction records with pagination"
)
def get_all_predictions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_postgres_session)
):
    """Get paginated list of all predictions."""
    try:
        query = text("""
            SELECT "PredictionID", "PatientID", "RawOutput", "PredictedClass", 
                   "PredictedLabel", "ModelVersion", "PredictedAt"
            FROM "Predictions"
            ORDER BY "PredictedAt" DESC
            OFFSET :skip LIMIT :limit
        """)
        
        results = db.execute(query, {"skip": skip, "limit": limit}).fetchall()
        
        predictions = []
        for row in results:
            predictions.append({
                "prediction_id": row[0],
                "patient_id": row[1],
                "raw_output": row[2],
                "predicted_class": row[3],
                "predicted_label": row[4],
                "model_version": row[5],
                "predicted_at": row[6].isoformat() if row[6] else None
            })
        
        # Get total count
        count_result = db.execute(text('SELECT COUNT(*) FROM "Predictions"')).scalar()
        
        return {
            "total": count_result,
            "skip": skip,
            "limit": limit,
            "predictions": predictions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/predictions/patient/{patient_id}",
    summary="Get predictions for specific patient",
    description="Retrieve all prediction records for a specific patient"
)
def get_predictions_for_patient(
    patient_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get all predictions for a specific patient."""
    try:
        query = text("""
            SELECT "PredictionID", "PatientID", "RawOutput", "PredictedClass", 
                   "PredictedLabel", "ModelVersion", "PredictedAt", "FeatureSnapshot"
            FROM "Predictions"
            WHERE "PatientID" = :patient_id
            ORDER BY "PredictedAt" DESC
        """)
        
        results = db.execute(query, {"patient_id": patient_id}).fetchall()
        
        if not results:
            return {
                "patient_id": patient_id,
                "total_predictions": 0,
                "predictions": []
            }
        
        predictions = []
        for row in results:
            predictions.append({
                "prediction_id": row[0],
                "patient_id": row[1],
                "raw_output": row[2],
                "predicted_class": row[3],
                "predicted_label": row[4],
                "model_version": row[5],
                "predicted_at": row[6].isoformat() if row[6] else None,
                "features": json.loads(row[7]) if row[7] else None
            })
        
        return {
            "patient_id": patient_id,
            "total_predictions": len(predictions),
            "predictions": predictions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

