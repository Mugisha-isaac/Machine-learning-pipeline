"""
FastAPI application entry point.
Example main file showing how to use the core database setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings, verify_connections
from app.api.postgres import routes as postgres_routes
from app.api.mongodb import routes as mongodb_routes

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Machine Learning Pipeline API for Healthcare Data",
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
