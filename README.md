# Machine Learning Pipeline

A healthcare machine learning pipeline API with PostgreSQL and MongoDB support.

## Features

- **PostgreSQL**: Structured healthcare data storage (patients, conditions, metrics, etc.)
- **MongoDB**: ML models, predictions, training jobs, and analytics storage
- **FastAPI**: Modern, fast API framework
- **SQLAlchemy**: ORM for PostgreSQL
- **Pydantic**: Data validation and settings management

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# PostgreSQL Configuration
POSTGRES_URL=postgresql://neondb_owner:**********@ep-icy-queen-adcehdzl-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# MongoDB Configuration
MONGO_URI=mongodb+srv://******:****@cluster0.5zu3lle.mongodb.net/?appName=Cluster0
MONGO_DB=healthcare_ml

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Machine Learning Pipeline
```

### 3. Database Setup

The PostgreSQL schema is defined in `dbdesign.sql`. You can run it against your database:

```bash
psql $POSTGRES_URL -f dbdesign.sql
```

## Project Structure

```
app/
├── api/              # API endpoints (to be implemented)
├── core/             # Core configuration and database
│   ├── config.py     # Settings and configuration
│   ├── database.py   # Database connections and sessions
│   ├── models.py     # PostgreSQL SQLAlchemy models
│   ├── mongo_models.py  # MongoDB Pydantic schemas
│   └── db_utils.py   # Database utility functions
└── ...
```

## Usage

### PostgreSQL (Structured Data)

The core module provides easy-to-use imports:

```python
from app.core import (
    get_postgres_session,
    Patient,
    HealthCondition,
    LifestyleFactor,
    HealthMetric,
    HealthcareAccess
)

# In FastAPI routes
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/patients")
def get_patients(db: Session = Depends(get_postgres_session)):
    return db.query(Patient).all()

# Outside FastAPI (using context manager)
from app.core import get_postgres_session_context

with get_postgres_session_context() as db:
    patients = db.query(Patient).all()
```

### MongoDB (ML Data)

```python
from app.core import (
    get_mongo_db,
    MLModel,
    Prediction,
    TrainingJob,
    COLLECTIONS
)

# Get MongoDB database
db = get_mongo_db()

# Access collections
models_collection = db[COLLECTIONS["ml_models"]]
predictions_collection = db[COLLECTIONS["predictions"]]

# Insert a model
model = MLModel(
    model_name="diabetes_predictor",
    model_type="classification",
    algorithm="random_forest",
    features=["Age", "BMI", "HighBP"],
    target="Diabetes_012"
)
model_dict = model.dict(by_alias=True)
models_collection.insert_one(model_dict)
```

## Database Schema

### PostgreSQL Tables

- **Patients**: Demographics (Sex, Age, Education, Income)
- **Health_Conditions**: Medical conditions (Diabetes, HighBP, Stroke, etc.)
- **Lifestyle_Factors**: Lifestyle metrics (BMI, Smoking, Physical Activity, etc.)
- **Health_Metrics**: Health screenings and self-reported metrics
- **Healthcare_Access**: Healthcare access information

### MongoDB Collections

- **ml_models**: ML model metadata and configurations
- **predictions**: Individual predictions made by models
- **training_jobs**: Training job tracking and status
- **analytics**: Analytics and insights from predictions
- **feature_importance**: Feature importance analysis

## Development

### Verify Connections

```python
from app.core import verify_connections

verify_connections()  # Tests both PostgreSQL and MongoDB
```

### Running the API

```bash
uvicorn app.main:app --reload
```

(Note: You'll need to create `app/main.py` with your FastAPI app)

## License

MIT

