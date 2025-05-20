from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.patient import PatientCreate, PatientUpdate, PatientInDB
from ...services.patient_service import PatientService
from ...db.mongodb import get_database

router = APIRouter()

def get_patient_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> PatientService:
    return PatientService(db)

@router.post("/", response_model=PatientInDB, status_code=201)
async def create_patient(
    patient: PatientCreate,
    patient_service: PatientService = Depends(get_patient_service)
):
    """Create a new patient"""
    return await patient_service.create_patient(patient)

@router.get("/{patient_id}", response_model=PatientInDB)
async def get_patient(
    patient_id: str,
    patient_service: PatientService = Depends(get_patient_service)
):
    """Get a patient by ID"""
    patient = await patient_service.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/", response_model=List[PatientInDB])
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    patient_service: PatientService = Depends(get_patient_service)
):
    """List patients with optional search and pagination"""
    return await patient_service.get_patients(skip=skip, limit=limit, search=search)

@router.put("/{patient_id}", response_model=PatientInDB)
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    patient_service: PatientService = Depends(get_patient_service)
):
    """Update a patient"""
    updated_patient = await patient_service.update_patient(patient_id, patient_update)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient

@router.delete("/{patient_id}", status_code=204)
async def delete_patient(
    patient_id: str,
    patient_service: PatientService = Depends(get_patient_service)
):
    """Delete a patient"""
    success = await patient_service.delete_patient(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found") 