from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.blood_test import BloodTestCreate, BloodTestUpdate, BloodTestInDB
from ...services.blood_test_service import BloodTestService
from ...db.mongodb import get_database

router = APIRouter()

def get_blood_test_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> BloodTestService:
    return BloodTestService(db)

@router.post("/", response_model=BloodTestInDB, status_code=201)
async def create_blood_test(
    blood_test: BloodTestCreate,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Create a new blood test record"""
    try:
        return await blood_test_service.create_blood_test(blood_test)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{test_id}", response_model=BloodTestInDB)
async def get_blood_test(
    test_id: str,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get a blood test by ID"""
    test = await blood_test_service.get_blood_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Blood test not found")
    return test

@router.get("/patient/{patient_id}", response_model=List[BloodTestInDB])
async def get_patient_blood_tests(
    patient_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    test_type: Optional[str] = None,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get all blood tests for a patient with optional filtering"""
    return await blood_test_service.get_patient_blood_tests(
        patient_id=patient_id,
        skip=skip,
        limit=limit,
        test_type=test_type
    )

@router.get("/patient/{patient_id}/latest", response_model=BloodTestInDB)
async def get_latest_blood_test(
    patient_id: str,
    test_type: Optional[str] = None,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get the latest blood test for a patient"""
    test = await blood_test_service.get_latest_blood_test(patient_id, test_type)
    if not test:
        raise HTTPException(status_code=404, detail="No blood tests found")
    return test

@router.put("/{test_id}", response_model=BloodTestInDB)
async def update_blood_test(
    test_id: str,
    blood_test_update: BloodTestUpdate,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Update a blood test record"""
    updated_test = await blood_test_service.update_blood_test(test_id, blood_test_update)
    if not updated_test:
        raise HTTPException(status_code=404, detail="Blood test not found")
    return updated_test

@router.delete("/{test_id}", status_code=204)
async def delete_blood_test(
    test_id: str,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Delete a blood test record"""
    success = await blood_test_service.delete_blood_test(test_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blood test not found")

@router.get("/patient/{patient_id}/statistics/{test_type}/{metric}", response_model=Dict)
async def get_test_statistics(
    patient_id: str,
    test_type: str,
    metric: str,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get statistics for a specific test metric over time"""
    return await blood_test_service.get_test_statistics(patient_id, test_type, metric)

@router.get("/patient/{patient_id}/recent", response_model=List[BloodTestInDB])
async def get_recent_blood_tests(
    patient_id: str,
    limit: int = Query(5, ge=1, le=50),
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get the most recent blood tests for a patient"""
    return await blood_test_service.get_patient_blood_tests(patient_id=patient_id, skip=0, limit=limit)

@router.get("/patient/{patient_id}/summary", response_model=Dict)
async def get_patient_blood_tests_summary(
    patient_id: str,
    metric: Optional[str] = None,
    blood_test_service: BloodTestService = Depends(get_blood_test_service)
):
    """Get summary statistics for a patient's blood tests: total count, count by type, and (optionally) average of a metric."""
    # Buscar todos os exames do paciente
    tests = await blood_test_service.get_patient_blood_tests(patient_id=patient_id, skip=0, limit=1000)
    summary = {
        "total_tests": len(tests),
        "count_by_type": {},
        "metric_avg": None
    }
    # Contagem por tipo
    for test in tests:
        ttype = test.test_type
        summary["count_by_type"][ttype] = summary["count_by_type"].get(ttype, 0) + 1
    # Média de um resultado específico
    if metric:
        values = [test.results.get(metric) for test in tests if metric in test.results]
        if values:
            summary["metric_avg"] = sum(values) / len(values)
    return summary 