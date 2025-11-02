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

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at: **http://localhost:8000**

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
├── dbdesign.sql                   # PostgreSQL schema
├── requirements.txt               # Python dependencies
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
curl -X POST "http://localhost:8000/api/v1/postgres/patients/" \
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
curl -X PUT "http://localhost:8000/api/v1/postgres/patients/1" \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 46,
    "Income": 80000
  }'
```

### Deleting a Patient

```bash
curl -X DELETE "http://localhost:8000/api/v1/postgres/patients/1"
```

### Using Python Requests

```python
import requests

# Create a patient
response = requests.post(
    "http://localhost:8000/api/v1/postgres/patients/",
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
    f"http://localhost:8000/api/v1/postgres/patients/{patient['PatientID']}",
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

Once the server is running, access:
- **Swagger UI**: http://localhost:8000 (interactive API documentation)
- **ReDoc**: http://localhost:8000/redoc (alternative documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json (machine-readable spec)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Contact

For issues, questions, or contributions, please open an issue on GitHub.

