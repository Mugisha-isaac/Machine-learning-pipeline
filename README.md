# Machine Learning Pipeline

A healthcare machine learning pipeline API with PostgreSQL and MongoDB support, providing RESTful endpoints for managing healthcare data.

## Features

- **Dual Database Support**: 
  - **PostgreSQL**: Structured healthcare data storage (patients, conditions, metrics, etc.)
  - **MongoDB**: NoSQL storage for flexible healthcare data modeling
- **FastAPI Framework**: Modern, fast, async-ready API with automatic OpenAPI documentation
- **SQLAlchemy ORM**: Type-safe PostgreSQL operations
- **Pydantic v2**: Data validation and serialization
- **CRUD Operations**: POST, PUT, DELETE endpoints for all entities (GET endpoints removed for write-only workflow)
- **Interactive Swagger UI**: Available at the root URL for easy API exploration

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# PostgreSQL Configuration
POSTGRES_URL=postgresql://username:password@host:port/database

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
# Or for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=healthcare_ml

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Machine Learning Pipeline
```

### 3. Database Setup

The PostgreSQL schema is defined in `dbdesign.sql`. Run it against your database:

```bash
psql $POSTGRES_URL -f dbdesign.sql
```

### 4. Run the Application

**Production Deployment**: The API is deployed and accessible at:
**https://machine-learning-pipeline.onrender.com**

For local development:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at: **https://machine-learning-pipeline.onrender.com** (production) or **http://localhost:8000** (local)

## Project Structure

```
ML pipeline/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   ├── postgres/              # PostgreSQL endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # POST/PUT/DELETE endpoints
│   │   │   ├── patients.py
│   │   │   ├── health_conditions.py
│   │   │   ├── health_metrics.py
│   │   │   ├── healthcare_access.py
│   │   │   ├── lifestyle_factors.py
│   │   │   ├── schemas.py         # Pydantic schemas
│   │   │   └── training_data.py
│   │   └── mongodb/               # MongoDB endpoints
│   │       ├── __init__.py
│   │       ├── routes.py          # POST/PUT/DELETE endpoints
│   │       ├── patients.py
│   │       ├── health_conditions.py
│   │       ├── health_metrics.py
│   │       ├── healthcare_access.py
│   │       ├── lifestyle_factors.py
│   │       └── training_data.py
│   └── core/                      # Core configuration and models
│       ├── __init__.py
│       ├── config.py              # Pydantic settings
│       ├── database.py            # Database connections
│       ├── models.py              # PostgreSQL SQLAlchemy models
│       └── mongo_models.py        # MongoDB Pydantic schemas
├── models/                        # Machine learning models
│   ├── model_exp5.h5             # Trained Keras/TensorFlow model
│   ├── scaler.joblib             # Feature scaler for normalization
│   └── feature_names.txt         # List of model features
├── scripts/                       # Utility scripts
│   ├── predict.py                # Diabetes prediction script
│   ├── train_model.py            # Model training script
│   └── sample_database.py        # Database population script
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_postgres_endpoints.py
│   ├── test_mongodb_endpoints.py
│   ├── test_integration.py
│   └── test_utils.py
├── dbdesign.sql                   # PostgreSQL schema
├── stored_procedures.sql          # SQL stored procedures
├── diabetes.csv                   # Training dataset
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
└── README.md
```

## API Endpoints

All endpoints are prefixed with `/api/v1`. The API provides **POST, PUT, and DELETE** operations only.

### PostgreSQL Endpoints (`/api/v1/postgres`)

#### Patients
- `POST /postgres/patients/` - Create a new patient
- `PUT /postgres/patients/{patient_id}` - Update patient information
- `DELETE /postgres/patients/{patient_id}` - Delete a patient

#### Health Conditions
- `POST /postgres/health-conditions/` - Create health condition record
- `PUT /postgres/health-conditions/{condition_id}` - Update health condition
- `DELETE /postgres/health-conditions/{condition_id}` - Delete health condition

#### Lifestyle Factors
- `POST /postgres/lifestyle-factors/` - Create lifestyle factor record
- `PUT /postgres/lifestyle-factors/{lifestyle_id}` - Update lifestyle factor
- `DELETE /postgres/lifestyle-factors/{lifestyle_id}` - Delete lifestyle factor

#### Health Metrics
- `POST /postgres/health-metrics/` - Create health metric record
- `PUT /postgres/health-metrics/{metric_id}` - Update health metric
- `DELETE /postgres/health-metrics/{metric_id}` - Delete health metric

#### Healthcare Access
- `POST /postgres/healthcare-access/` - Create healthcare access record
- `PUT /postgres/healthcare-access/{access_id}` - Update healthcare access
- `DELETE /postgres/healthcare-access/{access_id}` - Delete healthcare access

### MongoDB Endpoints (`/api/v1/mongodb`)

Same structure as PostgreSQL endpoints, with MongoDB ObjectId strings for identifiers:

- `POST /mongodb/patients/`
- `PUT /mongodb/patients/{patient_id}`
- `DELETE /mongodb/patients/{patient_id}`
- (Similar patterns for health-conditions, lifestyle-factors, health-metrics, healthcare-access)

## Usage Examples

### Creating a Patient (PostgreSQL)

```bash
curl -X POST "https://machine-learning-pipeline.onrender.com/api/v1/postgres/patients/" \
  -H "Content-Type: application/json" \
  -d '{
    "Sex": true,
    "Age": 45,
    "Education": 4,
    "Income": 75000
  }'
```

### Updating a Patient

```bash
curl -X PUT "https://machine-learning-pipeline.onrender.com/api/v1/postgres/patients/1" \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 46,
    "Income": 80000
  }'
```

### Deleting a Patient

```bash
curl -X DELETE "https://machine-learning-pipeline.onrender.com/api/v1/postgres/patients/1"
```

### Using Python Requests

```python
import requests

# Base URL for the API
API_BASE_URL = "https://machine-learning-pipeline.onrender.com/api/v1"

# Create a patient
response = requests.post(
    f"{API_BASE_URL}/postgres/patients/",
    json={
        "Sex": False,
        "Age": 32,
        "Education": 5,
        "Income": 65000
    }
)
patient = response.json()
print(f"Created patient with ID: {patient['PatientID']}")

# Update the patient
requests.put(
    f"{API_BASE_URL}/postgres/patients/{patient['PatientID']}",
    json={"Age": 33}
)
```

## Database Schema

### PostgreSQL Tables

All tables are related through foreign keys with the `Patients` table as the central entity.

#### Patients
Primary demographics table:
- `PatientID` (INT, Primary Key, Auto-increment)
- `Sex` (BOOLEAN) - 0 for female, 1 for male
- `Age` (INT)
- `Education` (INT) - Education level
- `Income` (INT) - Annual income

#### Health_Conditions
Medical conditions per patient:
- `ConditionID` (INT, Primary Key)
- `PatientID` (INT, Foreign Key)
- `Diabetes_012` (BOOLEAN) - 0=no diabetes, 1=prediabetes, 2=diabetes
- `HighBP` (BOOLEAN) - High blood pressure
- `HighChol` (BOOLEAN) - High cholesterol
- `Stroke` (BOOLEAN) - History of stroke
- `HeartDiseaseorAttack` (BOOLEAN)
- `DiffWalk` (BOOLEAN) - Difficulty walking

#### Lifestyle_Factors
Lifestyle and behavioral data:
- `LifestyleID` (INT, Primary Key)
- `PatientID` (INT, Foreign Key)
- `BMI` (FLOAT) - Body Mass Index
- `Smoker` (BOOLEAN)
- `PhysActivity` (BOOLEAN) - Regular physical activity
- `Fruits` (BOOLEAN) - Regular fruit consumption
- `Veggies` (BOOLEAN) - Regular vegetable consumption
- `HvyAlcoholConsump` (BOOLEAN) - Heavy alcohol consumption

#### Health_Metrics
Health screenings and self-reported metrics:
- `MetricsID` (INT, Primary Key)
- `PatientID` (INT, Foreign Key)
- `CholCheck` (BOOLEAN) - Cholesterol check in last 5 years
- `GenHlth` (INT) - General health (scale 1-5)
- `MentHlth` (INT) - Days of poor mental health in last 30 days
- `PhysHlth` (INT) - Days of poor physical health in last 30 days

#### Healthcare_Access
Healthcare accessibility information:
- `AccessID` (INT, Primary Key)
- `PatientID` (INT, Foreign Key)
- `AnyHealthcare` (BOOLEAN) - Has any healthcare coverage
- `NoDocbcCost` (BOOLEAN) - Could not see doctor due to cost

### MongoDB Collections

MongoDB collections mirror the PostgreSQL structure but with flexible schema support and timestamps:

- **Patients**: Patient demographics with embedded relationships (optional)
- **Health_Conditions**: Health condition records with created_at/updated_at
- **Lifestyle_Factors**: Lifestyle data with timestamps
- **Health_Metrics**: Health metrics with timestamps
- **Healthcare_Access**: Healthcare access data with timestamps

Each MongoDB document includes:
- `_id` (ObjectId) - MongoDB unique identifier
- `PatientID` (INT) - Reference to patient
- `created_at` (DateTime) - Record creation timestamp
- `updated_at` (DateTime) - Last update timestamp
- Additional fields matching PostgreSQL schema

## Machine Learning Prediction

### Using the Prediction Script

The project includes a diabetes prediction script (`scripts/predict.py`) that uses a trained neural network model to predict diabetes risk.

#### Prerequisites

- Trained model file: `models/model_exp5.h5`
- Scaler file: `models/scaler.joblib`
- Feature names: `models/feature_names.txt`

#### Running Predictions

```bash
cd scripts
python3 predict.py
```

#### Example Output

```
=== Diabetes Prediction System ===

✓ Model loaded successfully

✓ Example record fetched from API

Prepared feature vector:
  CholCheck: 1.0
  BMI: 25.0
  Smoker: 0.0
  Stroke: 0.0
  HeartDiseaseorAttack: 1.0
  PhysActivity: 1.0
  Fruits: 1.0
  Veggies: 0.0
  HvyAlcoholConsump: 0.0
  AnyHealthcare: 1.0
  NoDocbcCost: 0.0
  GenHlth: 2.0
  MentHlth: 0.0
  PhysHlth: 0.0
  DiffWalk: 0.0
  Sex: 0.0
  Age: 9.0
  Education: 6.0
  Income: 2.0

✓ Applied saved scaler

=== Prediction ===
Raw model output: 0.2183
Predicted class: 0 -> No Diabetes
==================
```

#### How It Works

1. **Fetches Training Data**: The script retrieves a sample record from the API endpoint
2. **Feature Preparation**: Normalizes and orders 21 features in the correct sequence
3. **Scaling**: Applies the saved StandardScaler for feature normalization
4. **Prediction**: Uses the trained Keras model to predict diabetes risk
5. **Interpretation**: Classifies output into three categories:
   - **0**: No Diabetes
   - **1**: Prediabetes
   - **2**: Diabetes

#### Configuration

The script uses environment variables for configuration:

```bash
# Set custom API endpoint (optional - defaults to production)
export TRAINING_EXAMPLE_API="https://machine-learning-pipeline.onrender.com/api/v1/postgres/training-data/latest"

# Run prediction
python3 scripts/predict.py
```

**Default API endpoint**: `https://machine-learning-pipeline.onrender.com/api/v1/postgres/training-data/latest`

### Using the Prediction API (Recommended)

The project now includes a comprehensive REST API for making predictions. This is the **recommended method** for production use.

#### Key Features

- ✅ Uses stored procedures (no external API calls)
- ✅ Model loaded once for better performance
- ✅ Supports single, latest, and batch predictions
- ✅ Automatic database logging
- ✅ RESTful interface for easy integration

#### API Endpoints

**Base URL**: `https://machine-learning-pipeline.onrender.com/api/v1/postgres/predictions`

1. **POST** `/predict/patient/{patient_id}` - Predict for specific patient
2. **POST** `/predict/latest` - Predict for latest patient
3. **POST** `/predict/batch` - Batch predictions (up to 100 patients)
4. **GET** `/predictions/` - Get all predictions (paginated)
5. **GET** `/predictions/patient/{patient_id}` - Get patient prediction history

#### Quick Examples

**Predict for Patient ID 1:**
```bash
curl -X POST "https://machine-learning-pipeline.onrender.com/api/v1/postgres/predictions/predict/patient/1"
```

**Predict for Latest Patient:**
```bash
curl -X POST "https://machine-learning-pipeline.onrender.com/api/v1/postgres/predictions/predict/latest"
```

**Batch Predictions:**
```bash
curl -X POST "https://machine-learning-pipeline.onrender.com/api/v1/postgres/predictions/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"patient_ids": [1, 2, 3, 4, 5]}'
```

**Python Example:**
```python
import requests

BASE_URL = "https://machine-learning-pipeline.onrender.com/api/v1/postgres/predictions"

# Single prediction
response = requests.post(f"{BASE_URL}/predict/patient/1")
result = response.json()

print(f"Prediction: {result['prediction']['predicted_label']}")
print(f"Raw Output: {result['prediction']['raw_output']:.4f}")
print(f"Logged as PredictionID: {result['prediction_id']}")
```

**Response Example:**
```json
{
  "success": true,
  "prediction_id": 15,
  "patient_id": 1,
  "prediction": {
    "raw_output": 0.2183,
    "predicted_class": 0,
    "predicted_label": "No Diabetes",
    "confidence": 0.2183
  },
  "model_version": "model_exp5",
  "predicted_at": "2025-11-02T14:23:45.123456",
  "features_used": { ... }
}
```

#### Full Documentation

For complete API documentation, examples, and integration guides, see:
- **[PREDICTION_API_GUIDE.md](PREDICTION_API_GUIDE.md)** - Comprehensive API documentation
- **Interactive Docs**: https://machine-learning-pipeline.onrender.com (Swagger UI)

## Development

### Connection Verification

Test both database connections:

```python
from app.core import verify_connections

try:
    verify_connections()
    print("✓ Both databases connected successfully")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

### Direct Database Access

#### PostgreSQL (with SQLAlchemy)

```python
from app.core.database import get_postgres_session
from app.core.models import Patient, HealthCondition

# Using dependency injection in FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/custom-query/")
def custom_query(db: Session = Depends(get_postgres_session)):
    # Complex queries with joins
    results = db.query(Patient, HealthCondition)\
        .join(HealthCondition)\
        .filter(Patient.Age > 40)\
        .all()
    return results

# Outside FastAPI (context manager)
from app.core.database import get_postgres_session_context

with get_postgres_session_context() as db:
    patients = db.query(Patient).filter(Patient.Age > 50).all()
```

#### MongoDB (with PyMongo)

```python
from app.core.database import get_mongo_db
from app.core.mongo_models import COLLECTIONS
from bson import ObjectId

db = get_mongo_db()

# Insert document
patient_data = {
    "PatientID": 123,
    "Sex": True,
    "Age": 45,
    "created_at": datetime.utcnow()
}
result = db[COLLECTIONS["patients"]].insert_one(patient_data)

# Find documents
patients = db[COLLECTIONS["patients"]].find({"Age": {"$gt": 40}})

# Update document
db[COLLECTIONS["patients"]].update_one(
    {"_id": ObjectId("...")},
    {"$set": {"Age": 46}}
)
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Tech Stack

- **FastAPI** 0.115.6 - Modern async web framework
- **SQLAlchemy** 2.0.36 - SQL ORM
- **Pydantic** 2.10.6 - Data validation
- **Pydantic Settings** 2.7.1 - Configuration management
- **PyMongo** 4.10.1 - MongoDB driver
- **Uvicorn** 0.34.0 - ASGI server
- **Python** 3.10+

## Troubleshooting

### Common Issues

**Import Errors**: Ensure Pydantic v2 and compatible versions are installed:
```bash
pip install pydantic==2.10.6 pydantic-settings==2.7.1 email-validator>=2.0
```

**Database Connection Failed**: 
- Verify `.env` file exists with correct credentials
- Check network connectivity to database servers
- Ensure databases are running and accessible

**Port Already in Use**:
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

## API Documentation

Access the live API documentation:
- **Swagger UI**: https://machine-learning-pipeline.onrender.com (interactive API documentation)
- **ReDoc**: https://machine-learning-pipeline.onrender.com/redoc (alternative documentation)
- **OpenAPI JSON**: https://machine-learning-pipeline.onrender.com/openapi.json (machine-readable spec)

For local development:
- **Swagger UI**: http://localhost:8000
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## License

MIT License - see LICENSE file for details

