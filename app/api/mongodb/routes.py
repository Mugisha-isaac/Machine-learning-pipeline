"""
MongoDB Main Router
Aggregates all MongoDB controller routes
"""
from fastapi import APIRouter

# Import all controller routers
from app.api.mongodb import (
    patients,
    health_conditions,
    lifestyle_factors,
    health_metrics,
    healthcare_access,
    training_data
)

# Main router for MongoDB operations (no tags to allow sub-router tags to show)
router = APIRouter(
    prefix="/mongodb",
    responses={404: {"description": "Not found"}},
)

# Include all sub-routers with their respective prefixes and tags
router.include_router(patients.router, prefix="/patients")
router.include_router(health_conditions.router, prefix="/health-conditions")
router.include_router(lifestyle_factors.router, prefix="/lifestyle-factors")
router.include_router(health_metrics.router, prefix="/health-metrics")
router.include_router(healthcare_access.router, prefix="/healthcare-access")
router.include_router(training_data.router, prefix="")
