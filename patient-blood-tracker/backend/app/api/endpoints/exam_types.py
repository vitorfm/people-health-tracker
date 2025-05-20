from fastapi import APIRouter, HTTPException, Depends
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.exam_type import ExamTypeCreate, ExamTypeUpdate, ExamTypeInDB
from ...db.mongodb import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[ExamTypeInDB])
async def list_exam_types(db: AsyncIOMotorDatabase = Depends(get_database)):
    items = await db.exam_types.find().to_list(100)
    return [ExamTypeInDB(**item) for item in items]

@router.post("/", response_model=ExamTypeInDB, status_code=201)
async def create_exam_type(data: ExamTypeCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    obj = data.dict()
    result = await db.exam_types.insert_one(obj)
    created = await db.exam_types.find_one({"_id": result.inserted_id})
    return ExamTypeInDB(**created)

@router.get("/{exam_type_id}", response_model=ExamTypeInDB)
async def get_exam_type(exam_type_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    item = await db.exam_types.find_one({"_id": ObjectId(exam_type_id)})
    if not item:
        raise HTTPException(status_code=404, detail="ExamType not found")
    return ExamTypeInDB(**item)

@router.put("/{exam_type_id}", response_model=ExamTypeInDB)
async def update_exam_type(exam_type_id: str, data: ExamTypeUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    await db.exam_types.update_one({"_id": ObjectId(exam_type_id)}, {"$set": update_data})
    updated = await db.exam_types.find_one({"_id": ObjectId(exam_type_id)})
    if not updated:
        raise HTTPException(status_code=404, detail="ExamType not found")
    return ExamTypeInDB(**updated)

@router.delete("/{exam_type_id}", status_code=204)
async def delete_exam_type(exam_type_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await db.exam_types.delete_one({"_id": ObjectId(exam_type_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ExamType not found") 