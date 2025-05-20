from datetime import datetime
from typing import List, Optional, Dict
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.blood_test import BloodTestCreate, BloodTestUpdate, BloodTestInDB

class BloodTestService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.blood_tests

    async def create_blood_test(self, blood_test: BloodTestCreate) -> BloodTestInDB:
        # Validação: garantir que o patient_id existe
        patient = await self.db.patients.find_one({"_id": ObjectId(blood_test.patient_id)})
        if not patient:
            raise ValueError("Patient not found for the provided patient_id.")
        # Validação: garantir que todos os exam_types existem
        for exam_type_id in blood_test.exam_types:
            exam_type = await self.db.exam_types.find_one({"_id": ObjectId(exam_type_id)})
            if not exam_type:
                raise ValueError(f"ExamType not found for id: {exam_type_id}")
        # Validação: garantir que o doctor_id existe (se informado)
        if blood_test.doctor_id:
            doctor = await self.db.doctors.find_one({"_id": ObjectId(blood_test.doctor_id)})
            if not doctor:
                raise ValueError(f"Doctor not found for id: {blood_test.doctor_id}")
        # Validação: garantir que todos os exam_type_id em results existem
        for result in blood_test.results:
            exam_type = await self.db.exam_types.find_one({"_id": ObjectId(result.exam_type_id)})
            if not exam_type:
                raise ValueError(f"ExamType not found for result exam_type_id: {result.exam_type_id}")
        blood_test_dict = blood_test.dict()
        blood_test_dict["created_at"] = datetime.utcnow()
        blood_test_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(blood_test_dict)
        created_test = await self.collection.find_one({"_id": result.inserted_id})
        
        return BloodTestInDB(**created_test)

    async def get_blood_test(self, test_id: str) -> Optional[BloodTestInDB]:
        if not ObjectId.is_valid(test_id):
            return None
            
        test = await self.collection.find_one({"_id": ObjectId(test_id)})
        return BloodTestInDB(**test) if test else None

    async def get_patient_blood_tests(
        self,
        patient_id: str,
        skip: int = 0,
        limit: int = 10,
        test_type: Optional[str] = None
    ) -> List[BloodTestInDB]:
        query = {"patient_id": patient_id}
        if test_type:
            query["test_type"] = test_type
            
        cursor = self.collection.find(query).sort("test_date", -1).skip(skip).limit(limit)
        tests = await cursor.to_list(length=limit)
        return [BloodTestInDB(**test) for test in tests]

    async def get_latest_blood_test(
        self,
        patient_id: str,
        test_type: Optional[str] = None
    ) -> Optional[BloodTestInDB]:
        query = {"patient_id": patient_id}
        if test_type:
            query["test_type"] = test_type
            
        test = await self.collection.find_one(
            query,
            sort=[("test_date", -1)]
        )
        return BloodTestInDB(**test) if test else None

    async def update_blood_test(
        self,
        test_id: str,
        blood_test_update: BloodTestUpdate
    ) -> Optional[BloodTestInDB]:
        if not ObjectId.is_valid(test_id):
            return None

        update_data = blood_test_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(test_id)},
            {"$set": update_data}
        )

        if result.modified_count:
            updated_test = await self.collection.find_one({"_id": ObjectId(test_id)})
            return BloodTestInDB(**updated_test)
        return None

    async def delete_blood_test(self, test_id: str) -> bool:
        if not ObjectId.is_valid(test_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(test_id)})
        return result.deleted_count > 0

    async def get_test_statistics(
        self,
        patient_id: str,
        test_type: str,
        metric: str
    ) -> Dict:
        """Get statistics for a specific test metric over time"""
        pipeline = [
            {"$match": {
                "patient_id": patient_id,
                "test_type": test_type
            }},
            {"$sort": {"test_date": 1}},
            {"$project": {
                "date": "$test_date",
                "value": f"$results.{metric}"
            }}
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        return {
            "metric": metric,
            "values": results
        } 