"""
MongoDB Pydantic schemas for healthcare data.
Mirrors the PostgreSQL models structure but designed for MongoDB.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class HealthCondition(BaseModel):
    """Patient health conditions (MongoDB version)."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    PatientID: int  # Reference to patient
    ConditionID: Optional[int] = None  # Can be used for migration/reference
    Diabetes_012: Optional[bool] = Field(None, description="0=no, 1=prediabetes, 2=diabetes")
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: str}


class LifestyleFactor(BaseModel):
    """Patient lifestyle factors (MongoDB version)."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    PatientID: int  # Reference to patient
    LifestyleID: Optional[int] = None  # Can be used for migration/reference
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: str}


class HealthMetric(BaseModel):
    """Patient health metrics and screenings (MongoDB version)."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    PatientID: int  # Reference to patient
    MetricsID: Optional[int] = None  # Can be used for migration/reference
    CholCheck: Optional[bool] = Field(None, description="Cholesterol check in last 5 years")
    GenHlth: Optional[int] = Field(None, description="Scale 1-5")
    MentHlth: Optional[int] = Field(None, description="Days of poor mental health in last 30 days")
    PhysHlth: Optional[int] = Field(None, description="Days of poor physical health in last 30 days")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: str}


class HealthcareAccess(BaseModel):
    """Patient healthcare access information (MongoDB version)."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    PatientID: int  # Reference to patient
    AccessID: Optional[int] = None  # Can be used for migration/reference
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = Field(None, description="Could not see doctor due to cost")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: str}


class Patient(BaseModel):
    """Patient demographic information (MongoDB version).
    
    In MongoDB, related data can be:
    1. Embedded (nested documents) - store related data directly in the patient document
    2. Referenced (IDs only) - store only IDs and populate when needed
    
    This schema supports both approaches with optional nested fields.
    """
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    PatientID: int  # Keep for compatibility with PostgreSQL
    Sex: Optional[bool] = Field(None, description="0 for female, 1 for male")
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None
    
    # Optional embedded relationships (MongoDB style)
    health_conditions: Optional[List[HealthCondition]] = None
    lifestyle_factors: Optional[List[LifestyleFactor]] = None
    health_metrics: Optional[List[HealthMetric]] = None
    healthcare_access: Optional[List[HealthcareAccess]] = None
    
    # Timestamps
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str, datetime: str}


# MongoDB Collection Names matching the PostgreSQL table names
COLLECTIONS = {
    "patients": "Patients",
    "health_conditions": "Health_Conditions",
    "lifestyle_factors": "Lifestyle_Factors",
    "health_metrics": "Health_Metrics",
    "healthcare_access": "Healthcare_Access",
}
