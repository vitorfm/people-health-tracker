from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field
from .objectid import PydanticObjectId

class ReferenceRange(BaseModel):
    min: float
    max: float

class ExamTypeBase(BaseModel):
    name: str
    reference_values: Dict[str, ReferenceRange]  # keys: 'male', 'female', 'child'
    description: str

class ExamTypeCreate(ExamTypeBase):
    pass

class ExamTypeUpdate(ExamTypeBase):
    name: str = None
    reference_values: Dict[str, ReferenceRange] = None
    description: str = None

class ExamTypeInDB(ExamTypeBase):
    id: PydanticObjectId = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 