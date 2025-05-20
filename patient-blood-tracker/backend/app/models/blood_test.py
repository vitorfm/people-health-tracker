from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .objectid import PydanticObjectId

class ExamResult(BaseModel):
    exam_type_id: str
    value: float

class BloodTestBase(BaseModel):
    patient_id: str
    test_date: datetime
    exam_types: List[str]  # List of ExamType IDs
    results: List[ExamResult]
    notes: Optional[str] = None
    doctor_id: Optional[str] = None
    lab_name: str

class BloodTestCreate(BloodTestBase):
    pass

class BloodTestUpdate(BloodTestBase):
    patient_id: Optional[str] = None
    test_date: Optional[datetime] = None
    exam_types: Optional[List[str]] = None
    results: Optional[List[ExamResult]] = None
    doctor_id: Optional[str] = None
    lab_name: Optional[str] = None
    notes: Optional[str] = None

class BloodTestInDB(BloodTestBase):
    id: PydanticObjectId = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 