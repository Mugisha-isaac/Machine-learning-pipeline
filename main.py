from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Machine Learning Pipeline API",
    description="API for diabetes prediction system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.diabetes_db

# Health check endpoint
@app.get("/api/v1/health-check")
async def health_check():
    return {"status": "healthy"}

# MongoDB routes
@app.get("/api/v1/mongodb/patients/latest")
async def get_latest_patients(limit: int = 10):
    patients = await db.patients.find().sort("_id", -1).limit(limit).to_list(limit)
    return {"patients": patients}

@app.get("/api/v1/mongodb/patients/by-patient-id/{patient_id}")
async def get_patient(patient_id: int):
    patient = await db.patients.find_one({"PatientID": patient_id})
    if patient:
        return patient
    return {"error": "Patient not found"}

@app.get("/api/v1/mongodb/health-conditions/patient/{patient_id}")
async def get_health_conditions(patient_id: int):
    conditions = await db.health_conditions.find_one({"PatientID": patient_id})
    return {"health_conditions": [conditions] if conditions else []}

@app.get("/api/v1/mongodb/lifestyle-factors/patient/{patient_id}")
async def get_lifestyle_factors(patient_id: int):
    factors = await db.lifestyle_factors.find_one({"PatientID": patient_id})
    return {"lifestyle_factors": [factors] if factors else []}

@app.get("/api/v1/mongodb/health-metrics/patient/{patient_id}")
async def get_health_metrics(patient_id: int):
    metrics = await db.health_metrics.find_one({"PatientID": patient_id})
    return {"health_metrics": [metrics] if metrics else []}

@app.get("/api/v1/mongodb/healthcare-access/patient/{patient_id}")
async def get_healthcare_access(patient_id: int):
    access = await db.healthcare_access.find_one({"PatientID": patient_id})
    return {"healthcare_access": [access] if access else []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
else:
    __all__ = ['app']