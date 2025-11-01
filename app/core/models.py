"""
SQLAlchemy models for PostgreSQL database.
Based on the schema defined in dbdesign.sql
"""
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Patient(Base):
    """Patient demographic information."""
    __tablename__ = "Patients"
    
    PatientID = Column(Integer, primary_key=True, autoincrement=True)
    Sex = Column(Boolean, nullable=True, comment="0 for female, 1 for male")
    Age = Column(Integer, nullable=True)
    Education = Column(Integer, nullable=True)
    Income = Column(Integer, nullable=True)
    
    # Relationships
    health_conditions = relationship("HealthCondition", back_populates="patient", cascade="all, delete-orphan")
    lifestyle_factors = relationship("LifestyleFactor", back_populates="patient", cascade="all, delete-orphan")
    health_metrics = relationship("HealthMetric", back_populates="patient", cascade="all, delete-orphan")
    healthcare_access = relationship("HealthcareAccess", back_populates="patient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Patient(PatientID={self.PatientID}, Age={self.Age}, Sex={self.Sex})>"


class HealthCondition(Base):
    """Patient health conditions."""
    __tablename__ = "Health_Conditions"
    
    ConditionID = Column(Integer, primary_key=True, autoincrement=True)
    PatientID = Column(Integer, ForeignKey("Patients.PatientID"), nullable=False)
    Diabetes_012 = Column(Boolean, nullable=True, comment="0=no, 1=prediabetes, 2=diabetes")
    HighBP = Column(Boolean, nullable=True)
    HighChol = Column(Boolean, nullable=True)
    Stroke = Column(Boolean, nullable=True)
    HeartDiseaseorAttack = Column(Boolean, nullable=True)
    DiffWalk = Column(Boolean, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="health_conditions")
    
    def __repr__(self):
        return f"<HealthCondition(ConditionID={self.ConditionID}, PatientID={self.PatientID})>"


class LifestyleFactor(Base):
    """Patient lifestyle factors."""
    __tablename__ = "Lifestyle_Factors"
    
    LifestyleID = Column(Integer, primary_key=True, autoincrement=True)
    PatientID = Column(Integer, ForeignKey("Patients.PatientID"), nullable=False)
    BMI = Column(Float, nullable=True)
    Smoker = Column(Boolean, nullable=True)
    PhysActivity = Column(Boolean, nullable=True)
    Fruits = Column(Boolean, nullable=True)
    Veggies = Column(Boolean, nullable=True)
    HvyAlcoholConsump = Column(Boolean, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="lifestyle_factors")
    
    def __repr__(self):
        return f"<LifestyleFactor(LifestyleID={self.LifestyleID}, PatientID={self.PatientID}, BMI={self.BMI})>"


class HealthMetric(Base):
    """Patient health metrics and screenings."""
    __tablename__ = "Health_Metrics"
    
    MetricsID = Column(Integer, primary_key=True, autoincrement=True)
    PatientID = Column(Integer, ForeignKey("Patients.PatientID"), nullable=False)
    CholCheck = Column(Boolean, nullable=True, comment="Cholesterol check in last 5 years")
    GenHlth = Column(Integer, nullable=True, comment="Scale 1-5")
    MentHlth = Column(Integer, nullable=True, comment="Days of poor mental health in last 30 days")
    PhysHlth = Column(Integer, nullable=True, comment="Days of poor physical health in last 30 days")
    
    # Relationships
    patient = relationship("Patient", back_populates="health_metrics")
    
    def __repr__(self):
        return f"<HealthMetric(MetricsID={self.MetricsID}, PatientID={self.PatientID})>"


class HealthcareAccess(Base):
    """Patient healthcare access information."""
    __tablename__ = "Healthcare_Access"
    
    AccessID = Column(Integer, primary_key=True, autoincrement=True)
    PatientID = Column(Integer, ForeignKey("Patients.PatientID"), nullable=False)
    AnyHealthcare = Column(Boolean, nullable=True)
    NoDocbcCost = Column(Boolean, nullable=True, comment="Could not see doctor due to cost")
    
    # Relationships
    patient = relationship("Patient", back_populates="healthcare_access")
    
    def __repr__(self):
        return f"<HealthcareAccess(AccessID={self.AccessID}, PatientID={self.PatientID})>"

