from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field

class BloodTestBase(BaseModel):
    patient_id: str
    test_date: datetime
    test_type: str
    results: Dict[str, float]
    reference_range: Dict[str, Dict[str, float]]
    notes: Optional[str] = None
    doctor_name: str
    lab_name: str

class BloodTestCreate(BloodTestBase):
    pass

class BloodTestUpdate(BloodTestBase):
    patient_id: Optional[str] = None
    test_date: Optional[datetime] = None
    test_type: Optional[str] = None
    results: Optional[Dict[str, float]] = None
    reference_range: Optional[Dict[str, Dict[str, float]]] = None
    doctor_name: Optional[str] = None
    lab_name: Optional[str] = None

class BloodTestInDB(BloodTestBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 