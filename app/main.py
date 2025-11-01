"""
FastAPI application entry point.
Example main file showing how to use the core database setup.
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core import (
    settings,
    get_postgres_session,
    get_mongo_db,
    verify_connections,
    Patient,
    HealthCondition,
    MLModel,
    COLLECTIONS,
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Machine Learning Pipeline API for Healthcare Data",
)


@app.on_event("startup")
async def startup_event():
    """Verify database connections on startup."""
    try:
        verify_connections()
    except Exception as e:
        print(f"Warning: Database connection check failed: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Machine Learning Pipeline API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        verify_connections()
        return {"status": "healthy", "databases": ["postgresql", "mongodb"]}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}




