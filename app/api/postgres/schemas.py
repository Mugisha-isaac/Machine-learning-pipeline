"""
PostgreSQL Pydantic Schemas
Request and response models for PostgreSQL API endpoints
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Generic, TypeVar

T = TypeVar('T')

# ==================== PAGINATION SCHEMA ====================

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


# ==================== PATIENT SCHEMAS ====================

class PatientCreate(BaseModel):
    Sex: Optional[bool] = None
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None


class PatientResponse(BaseModel):
    PatientID: int
    Sex: Optional[bool] = None
    Age: Optional[int] = None
    Education: Optional[int] = None
    Income: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class PatientsListResponse(BaseModel):
    """Paginated list of patients"""
    items: List[PatientResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ==================== HEALTH CONDITION SCHEMAS ====================

class HealthConditionCreate(BaseModel):
    PatientID: int
    Diabetes_012: Optional[bool] = None
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None


class HealthConditionResponse(BaseModel):
    ConditionID: int
    PatientID: int
    Diabetes_012: Optional[bool] = None
    HighBP: Optional[bool] = None
    HighChol: Optional[bool] = None
    Stroke: Optional[bool] = None
    HeartDiseaseorAttack: Optional[bool] = None
    DiffWalk: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== LIFESTYLE FACTOR SCHEMAS ====================

class LifestyleFactorCreate(BaseModel):
    PatientID: int
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None


class LifestyleFactorResponse(BaseModel):
    LifestyleID: int
    PatientID: int
    BMI: Optional[float] = None
    Smoker: Optional[bool] = None
    PhysActivity: Optional[bool] = None
    Fruits: Optional[bool] = None
    Veggies: Optional[bool] = None
    HvyAlcoholConsump: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== HEALTH METRIC SCHEMAS ====================

class HealthMetricCreate(BaseModel):
    PatientID: int
    CholCheck: Optional[bool] = None
    GenHlth: Optional[int] = None
    MentHlth: Optional[int] = None
    PhysHlth: Optional[int] = None


class HealthMetricResponse(BaseModel):
    MetricsID: int
    PatientID: int
    CholCheck: Optional[bool] = None
    GenHlth: Optional[int] = None
    MentHlth: Optional[int] = None
    PhysHlth: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# ==================== HEALTHCARE ACCESS SCHEMAS ====================

class HealthcareAccessCreate(BaseModel):
    PatientID: int
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = None


class HealthcareAccessResponse(BaseModel):
    AccessID: int
    PatientID: int
    AnyHealthcare: Optional[bool] = None
    NoDocbcCost: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)
