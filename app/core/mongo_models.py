"""
MongoDB Pydantic schemas for healthcare data.
Mirrors the PostgreSQL models structure but designed for MongoDB.
"""
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2."""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ], serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        ))

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


# Request schemas (for POST/PUT - no _id field)
class HealthConditionCreate(BaseModel):
    """Schema for creating health conditions."""
    PatientID: int
    ConditionID: Optional[int] = None
    Diabetes_012: Optional[bool] = Field(None, description="0=no, 1=prediabetes, 2=diabetes")
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class HealthConditionUpdate(BaseModel):
    """Schema for updating health conditions."""
    PatientID: Optional[int] = None
    ConditionID: Optional[int] = None
    Diabetes_012: Optional[bool] = Field(None, description="0=no, 1=prediabetes, 2=diabetes")
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


# Response schema (includes _id)
class HealthCondition(BaseModel):
    """Patient health conditions (MongoDB version) - Response schema."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    PatientID: int
    ConditionID: Optional[int] = None
    Diabetes_012: Optional[bool] = Field(None, description="0=no, 1=prediabetes, 2=diabetes")
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: str}
    )


class LifestyleFactorCreate(BaseModel):
    """Schema for creating lifestyle factors."""
    PatientID: int
    LifestyleID: Optional[int] = None
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class LifestyleFactorUpdate(BaseModel):
    """Schema for updating lifestyle factors."""
    PatientID: Optional[int] = None
    LifestyleID: Optional[int] = None
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class LifestyleFactor(BaseModel):
    """Patient lifestyle factors (MongoDB version) - Response schema."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    PatientID: int
    LifestyleID: Optional[int] = None
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: str}
    )


class HealthMetricCreate(BaseModel):
    """Schema for creating health metrics."""
    PatientID: int
    MetricsID: Optional[int] = None
    CholCheck: Optional[bool] = Field(None, description="Cholesterol check in last 5 years")
    GenHlth: Optional[int] = Field(None, description="Scale 1-5")
    MentHlth: Optional[int] = Field(None, description="Days of poor mental health in last 30 days")
    PhysHlth: Optional[int] = Field(None, description="Days of poor physical health in last 30 days")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class HealthMetricUpdate(BaseModel):
    """Schema for updating health metrics."""
    PatientID: Optional[int] = None
    MetricsID: Optional[int] = None
    CholCheck: Optional[bool] = Field(None, description="Cholesterol check in last 5 years")
    GenHlth: Optional[int] = Field(None, description="Scale 1-5")
    MentHlth: Optional[int] = Field(None, description="Days of poor mental health in last 30 days")
    PhysHlth: Optional[int] = Field(None, description="Days of poor physical health in last 30 days")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class HealthMetric(BaseModel):
    """Patient health metrics and screenings (MongoDB version) - Response schema."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    PatientID: int
    MetricsID: Optional[int] = None
    CholCheck: Optional[bool] = Field(None, description="Cholesterol check in last 5 years")
    GenHlth: Optional[int] = Field(None, description="Scale 1-5")
    MentHlth: Optional[int] = Field(None, description="Days of poor mental health in last 30 days")
    PhysHlth: Optional[int] = Field(None, description="Days of poor physical health in last 30 days")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: str}
    )


class HealthcareAccessCreate(BaseModel):
    """Schema for creating healthcare access records."""
    PatientID: int
    AccessID: Optional[int] = None
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = Field(None, description="Could not see doctor due to cost")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class HealthcareAccessUpdate(BaseModel):
    """Schema for updating healthcare access records."""
    PatientID: Optional[int] = None
    AccessID: Optional[int] = None
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = Field(None, description="Could not see doctor due to cost")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class HealthcareAccess(BaseModel):
    """Patient healthcare access information (MongoDB version) - Response schema."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    PatientID: int
    AccessID: Optional[int] = None
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = Field(None, description="Could not see doctor due to cost")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: str}
    )


class PatientCreate(BaseModel):
    """Schema for creating patients."""
    PatientID: int
    Sex: Optional[bool] = Field(None, description="0 for female, 1 for male")
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class PatientUpdate(BaseModel):
    """Schema for updating patients."""
    PatientID: Optional[int] = None
    Sex: Optional[bool] = Field(None, description="0 for female, 1 for male")
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Patient(BaseModel):
    """Patient demographic information (MongoDB version) - Response schema."""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    PatientID: int
    Sex: Optional[bool] = Field(None, description="0 for female, 1 for male")
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None

    # Optional embedded relationships
    health_conditions: Optional[List[HealthCondition]] = None
    lifestyle_factors: Optional[List[LifestyleFactor]] = None
    health_metrics: Optional[List[HealthMetric]] = None
    healthcare_access: Optional[List[HealthcareAccess]] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str, datetime: str}
    )


# MongoDB Collection Names
COLLECTIONS = {
    "patients": "Patients",
    "health_conditions": "Health_Conditions",
    "lifestyle_factors": "Lifestyle_Factors",
    "health_metrics": "Health_Metrics",
    "healthcare_access": "Healthcare_Access",
}
