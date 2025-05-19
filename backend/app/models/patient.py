from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from .objectid import PydanticObjectId

class PatientBase(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: datetime
    gender: str
    phone: str
    address: str
    diseases: List[str] = []
    notes: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    diseases: Optional[List[str]] = None
    notes: Optional[str] = None

class PatientInDB(PatientBase):
    id: PydanticObjectId = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        validate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        } 