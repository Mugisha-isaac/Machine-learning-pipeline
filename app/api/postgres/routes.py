from fastapi import APIRouter

from app.api.postgres import (
    patients,
    health_conditions,
    lifestyle_factors,
    health_metrics,
    healthcare_access,
    training_data,
    logs
)

router = APIRouter(
    prefix="/postgres",
    responses={404: {"description": "Not found"}},
)

# Include all sub-routers
router.include_router(patients.router, prefix="/patients")
router.include_router(health_conditions.router, prefix="/health-conditions")
router.include_router(lifestyle_factors.router, prefix="/lifestyle-factors")
router.include_router(health_metrics.router, prefix="/health-metrics")
router.include_router(healthcare_access.router, prefix="/healthcare-access")
router.include_router(training_data.router, prefix="/training-data")
router.include_router(logs.router, prefix="/logs")
