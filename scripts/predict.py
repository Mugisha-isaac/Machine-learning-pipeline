import os
import sys
import warnings
from pathlib import Path
import json
from datetime import datetime

# Suppress TensorFlow verbose logs
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
warnings.filterwarnings("ignore")

import requests
import numpy as np
from tensorflow.keras.models import load_model
import joblib
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Configuration
API_URL = os.getenv(
    "TRAINING_EXAMPLE_API",
    "https://machine-learning-pipeline.onrender.com/api/v1/postgres/training-data/latest"
)
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_exp5.h5"
SCALER_PATH = Path(__file__).resolve().parents[1] / "models" / "scaler.joblib"
MODEL_VERSION = "model_exp5"

# Database connection string
DB_URL = os.getenv("POSTGRES_URL")  # PostgreSQL connection URL from .env

# Feature order expected by the model (must match training)
FEATURE_ORDER = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
    "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits",
    "Veggies", "HvyAlcoholConsump", "AnyHealthcare",
    "NoDocbcCost", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk",
    "Sex", "Age", "Education", "Income"
]

LABELS = {0: "No Diabetes", 1: "Prediabetes", 2: "Diabetes"}


def fetch_example_record(api_url: str, limit: int = 1, timeout: int = 10) -> dict:
    params = {"limit": limit}
    try:
        resp = requests.get(api_url, params=params, timeout=timeout)
    except requests.RequestException as e:
        raise RuntimeError(f"Network error when calling API: {e}")
    # Check HTTP status
    if resp.status_code != 200:
        # show short response body to aid debugging
        body = (resp.text or "")[:1000]
        raise RuntimeError(f"API returned status {resp.status_code}: {body}")
    text = (resp.text or "").strip()
    if not text:
        raise RuntimeError("API returned empty response body")
    try:
        data = resp.json()
    except ValueError:
        # Non-JSON response — include a snippet for debugging
        snippet = text[:1000]
        raise RuntimeError(f"API returned non-JSON response: {snippet}")

    # Try to find a record in common envelope keys
    record = None
    if isinstance(data, dict):
        for key in ("results", "rows", "data", "training_data", "items", "records", "patients"):
            if key in data and isinstance(data[key], list) and data[key]:
                record = data[key][0]
                break
        if record is None:
            # fallback: first list or dict found in values
            for v in data.values():
                if isinstance(v, list) and v:
                    record = v[0]
                    break
                if isinstance(v, dict):
                    record = v
                    break
    elif isinstance(data, list) and data:
        record = data[0]

    if not record:
        raise RuntimeError(f"No record found in API response: {data}")
    return record


def normalize_value(v):
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    if v is None:
        return 0.0
    try:
        return float(v)
    except Exception:
        return 0.0


def build_feature_vector(record: dict, feature_order: list) -> np.ndarray:
    vec = [normalize_value(record.get(f)) for f in feature_order]
    return np.array(vec, dtype=np.float32).reshape(1, -1)


def load_scaler(path: Path):
    if path.exists():
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None


def interpret_prediction(value: float) -> (int, str):
    # round to nearest integer class 0/1/2
    cls = int(np.clip(np.rint(value), 0, 2))
    label = LABELS.get(cls, f"Class {cls}")
    return cls, label


def log_prediction_to_db(patient_id: int, raw_output: float, predicted_class: int, 
                         predicted_label: str, feature_data: dict, model_version: str = MODEL_VERSION):
    """
    Log prediction results to the Predictions table in PostgreSQL.
    
    Args:
        patient_id: ID of the patient
        raw_output: Raw model output value
        predicted_class: Predicted class (0, 1, or 2)
        predicted_label: Human-readable label
        feature_data: Dictionary of input features
        model_version: Version of the model used
    
    Returns:
        prediction_id: ID of the inserted prediction record, or None if failed
    """
    if not DB_URL:
        print("⚠ Warning: POSTGRES_URL not set in environment. Skipping database logging.")
        return None
    
    try:
        # Connect to database
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        
        # Prepare feature snapshot as JSON
        feature_snapshot = json.dumps(feature_data)
        
        # Insert prediction record
        insert_query = """
            INSERT INTO "Predictions" 
            ("PatientID", "RawOutput", "PredictedClass", "PredictedLabel", 
             "ModelVersion", "PredictedAt", "FeatureSnapshot")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING "PredictionID"
        """
        
        cursor.execute(insert_query, (
            patient_id,
            raw_output,
            predicted_class,
            predicted_label,
            model_version,
            datetime.utcnow(),
            feature_snapshot
        ))
        
        prediction_id = cursor.fetchone()[0]
        
        # Commit transaction
        conn.commit()
        cursor.close()
        conn.close()
        
        return prediction_id
    
    except Exception as e:
        print(f"⚠ Error logging prediction to database: {e}")
        return None


def main():
    print("\n=== Diabetes Prediction System ===\n")

    # Load model
    if not MODEL_PATH.exists():
        print(f" Model not found at {MODEL_PATH}")
        sys.exit(1)

    try:
        model = load_model(MODEL_PATH, compile=False)
        print("✓ Model loaded successfully\n")
    except Exception as e:
        print(f" Failed to load model: {e}")
        sys.exit(1)

    # Fetch example record from remote API
    try:
        record = fetch_example_record(API_URL, limit=1)
        print("✓ Example record fetched from API\n")
    except Exception as e:
        print(f"\n Error during prediction: {e}")
        sys.exit(1)

    # Build features
    feature_vector = build_feature_vector(record, FEATURE_ORDER)
    print("Prepared feature vector:")
    for name, val in zip(FEATURE_ORDER, feature_vector.flatten().tolist()):
        print(f"  {name}: {val}")
    print("")

    # Load scaler if available
    scaler = load_scaler(SCALER_PATH)
    if scaler:
        try:
            feature_vector = scaler.transform(feature_vector)
            print("✓ Applied saved scaler\n")
        except Exception as e:
            print(f"⚠ Failed to apply scaler: {e} -- proceeding without scaling\n")
    else:
        print("⚠ No scaler found; proceeding without scaling\n")

    # Make prediction
    try:
        pred = model.predict(feature_vector, verbose=0)
        # model may return shape (1,1) or (1,) or (1,n)
        raw_value = float(np.asarray(pred).reshape(-1)[0])
        cls, label = interpret_prediction(raw_value)
        print("=== Prediction ===")
        print(f"Raw model output: {raw_value:.4f}")
        print(f"Predicted class: {cls} -> {label}")
        print("==================\n")
    except Exception as e:
        print(f" Prediction failed: {e}")
        sys.exit(1)

    # Log prediction to database
    patient_id = record.get("PatientID")
    if patient_id:
        # Prepare feature data for logging
        feature_data = {name: val for name, val in zip(FEATURE_ORDER, feature_vector.flatten().tolist())}
        
        print("Logging prediction to database...")
        prediction_id = log_prediction_to_db(
            patient_id=patient_id,
            raw_output=raw_value,
            predicted_class=cls,
            predicted_label=label,
            feature_data=feature_data,
            model_version=MODEL_VERSION
        )
        
        if prediction_id:
            print(f"✓ Prediction logged successfully (PredictionID: {prediction_id})\n")
        else:
            print("⚠ Failed to log prediction to database\n")
    else:
        print("⚠ No PatientID found in record. Skipping database logging.\n")


if __name__ == "__main__":
    main()