from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_postgres_session
from app.core import models
from app.api.postgres.schemas import LifestyleFactorCreate, LifestyleFactorResponse

router = APIRouter(tags=["PostgreSQL - Lifestyle Factors"])


@router.get("/",
    response_model=List[LifestyleFactorResponse],
    summary="Get all lifestyle factors",
    description="Retrieve all lifestyle factor records with optional pagination"
)
def get_all_lifestyle_factors(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).offset(skip).limit(limit).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/latest",
    response_model=List[LifestyleFactorResponse],
    summary="Get latest lifestyle factors",
    description="Retrieve the most recently created lifestyle factor records"
)
def get_latest_lifestyle_factors(limit: int = 10, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).order_by(models.LifestyleFactor.LifestyleID.desc()).limit(limit).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/patient/{patient_id}",
    response_model=List[LifestyleFactorResponse],
    summary="Get lifestyle factors by PatientID",
    description="Retrieve all lifestyle factors for a specific patient"
)
def get_lifestyle_factors_by_patient(patient_id: int, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle_factors = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.PatientID == patient_id).all()
        return lifestyle_factors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{lifestyle_id}",
    response_model=LifestyleFactorResponse,
    summary="Get lifestyle factor by ID",
    description="Retrieve a single lifestyle factor record by ID"
)
def get_lifestyle_factor_by_id(lifestyle_id: int, db: Session = Depends(get_postgres_session)):
    try:
        lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
        if not lifestyle:
            raise HTTPException(status_code=404, detail="Lifestyle factor not found")
        return lifestyle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/",
    response_model=LifestyleFactorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new lifestyle factor",
    description="Create a new lifestyle factor record in PostgreSQL"
)
def create_lifestyle_factor(lifestyle: LifestyleFactorCreate, db: Session = Depends(get_postgres_session)):
    try:
        db_lifestyle = models.LifestyleFactor(**lifestyle.dict())
        db.add(db_lifestyle)
        db.commit()
        db.refresh(db_lifestyle)
        return db_lifestyle
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{lifestyle_id}", response_model=LifestyleFactorResponse)
def update_lifestyle_factor(lifestyle_id: int, lifestyle: LifestyleFactorCreate, db: Session = Depends(get_postgres_session)):
    db_lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
    if not db_lifestyle:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    
    for field, value in lifestyle.dict(exclude_unset=True).items():
        setattr(db_lifestyle, field, value)
    db.commit()
    db.refresh(db_lifestyle)
    return db_lifestyle


@router.delete("/{lifestyle_id}")
def delete_lifestyle_factor(lifestyle_id: int, db: Session = Depends(get_postgres_session)):
    db_lifestyle = db.query(models.LifestyleFactor).filter(models.LifestyleFactor.LifestyleID == lifestyle_id).first()
    if not db_lifestyle:
        raise HTTPException(status_code=404, detail="Lifestyle factor not found")
    db.delete(db_lifestyle)
    db.commit()
    return {"message": "Lifestyle factor deleted successfully"}
