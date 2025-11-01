"""
FastAPI application entry point.
Example main file showing how to use the core database setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings, verify_connections
from app.api.postgres import routes as postgres_routes
from app.api.mongodb import routes as mongodb_routes

# Define tags metadata for API documentation
tags_metadata = [
    # MongoDB Operations
    {
        "name": "MongoDB - Patients",
        "description": "Manage patient demographic records including age, sex, education, and income in MongoDB.",
    },
    {
        "name": "MongoDB - Health Conditions",
        "description": "Manage patient health conditions including diabetes, blood pressure, cholesterol, stroke, and heart disease in MongoDB.",
    },
    {
        "name": "MongoDB - Lifestyle Factors",
        "description": "Manage lifestyle data including BMI, smoking, physical activity, diet, and alcohol consumption in MongoDB.",
    },
    {
        "name": "MongoDB - Health Metrics",
        "description": "Manage health screening metrics including cholesterol checks, general health, mental health, and physical health in MongoDB.",
    },
    {
        "name": "MongoDB - Healthcare Access",
        "description": "Manage healthcare access information including insurance coverage and cost barriers in MongoDB.",
    },
    {
        "name": "MongoDB - Training Data",
        "description": "Aggregate and retrieve flattened patient data for machine learning model training from MongoDB.",
    },
    # PostgreSQL Operations
    {
        "name": "PostgreSQL - Patients",
        "description": "Manage patient demographic records including age, sex, education, and income in PostgreSQL.",
    },
    {
        "name": "PostgreSQL - Health Conditions",
        "description": "Manage patient health conditions including diabetes, blood pressure, cholesterol, stroke, and heart disease in PostgreSQL.",
    },
    {
        "name": "PostgreSQL - Lifestyle Factors",
        "description": "Manage lifestyle data including BMI, smoking, physical activity, diet, and alcohol consumption in PostgreSQL.",
    },
    {
        "name": "PostgreSQL - Health Metrics",
        "description": "Manage health screening metrics including cholesterol checks, general health, mental health, and physical health in PostgreSQL.",
    },
    {
        "name": "PostgreSQL - Healthcare Access",
        "description": "Manage healthcare access information including insurance coverage and cost barriers in PostgreSQL.",
    },
    {
        "name": "PostgreSQL - Training Data",
        "description": "Aggregate and retrieve complete patient records for machine learning model training from PostgreSQL.",
    },
]

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Machine Learning Pipeline API for Healthcare Data",
    openapi_tags=tags_metadata,
    docs_url="/",  # Swagger UI will be the landing page
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(postgres_routes.router, prefix="/api/v1")
app.include_router(mongodb_routes.router, prefix="/api/v1")

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
