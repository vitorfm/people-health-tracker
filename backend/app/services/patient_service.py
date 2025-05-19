from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.patient import PatientCreate, PatientUpdate, PatientInDB

class PatientService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.patients

    async def create_patient(self, patient: PatientCreate) -> PatientInDB:
        patient_dict = patient.dict()
        patient_dict["created_at"] = datetime.utcnow()
        patient_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(patient_dict)
        created_patient = await self.collection.find_one({"_id": result.inserted_id})
        
        return PatientInDB(**created_patient)

    async def get_patient(self, patient_id: str) -> Optional[PatientInDB]:
        if not ObjectId.is_valid(patient_id):
            return None
            
        patient = await self.collection.find_one({"_id": ObjectId(patient_id)})
        return PatientInDB(**patient) if patient else None

    async def get_patients(
        self, 
        skip: int = 0, 
        limit: int = 10,
        search: Optional[str] = None
    ) -> List[PatientInDB]:
        query = {}
        if search:
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}}
                ]
            }
            
        cursor = self.collection.find(query).skip(skip).limit(limit)
        patients = await cursor.to_list(length=limit)
        return [PatientInDB(**patient) for patient in patients]

    async def update_patient(
        self, 
        patient_id: str, 
        patient_update: PatientUpdate
    ) -> Optional[PatientInDB]:
        if not ObjectId.is_valid(patient_id):
            return None

        update_data = patient_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        result = await self.collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": update_data}
        )

        if result.modified_count:
            updated_patient = await self.collection.find_one({"_id": ObjectId(patient_id)})
            return PatientInDB(**updated_patient)
        return None

    async def delete_patient(self, patient_id: str) -> bool:
        if not ObjectId.is_valid(patient_id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(patient_id)})
        return result.deleted_count > 0 