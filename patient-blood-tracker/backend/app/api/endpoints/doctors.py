from fastapi import APIRouter, HTTPException, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.doctor import Doctor
from ...db.mongodb import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Doctor])
async def list_doctors(db: AsyncIOMotorDatabase = Depends(get_database)):
    items = await db.doctors.find().to_list(100)
    return [Doctor(**item) for item in items]

@router.post("/", response_model=Doctor, status_code=201)
async def create_doctor(data: Doctor, db: AsyncIOMotorDatabase = Depends(get_database)):
    obj = data.dict()
    result = await db.doctors.insert_one(obj)
    created = await db.doctors.find_one({"_id": result.inserted_id})
    return Doctor(**created)

@router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    item = await db.doctors.find_one({"_id": ObjectId(doctor_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return Doctor(**item)

@router.put("/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: str, data: Doctor, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    await db.doctors.update_one({"_id": ObjectId(doctor_id)}, {"$set": update_data})
    updated = await db.doctors.find_one({"_id": ObjectId(doctor_id)})
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return Doctor(**updated)

@router.delete("/{doctor_id}", status_code=204)
async def delete_doctor(doctor_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db.doctors.delete_one({"_id": ObjectId(doctor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found") 