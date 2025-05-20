from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Person(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: datetime
    gender: str
    phone: str
    address: str
    notes: Optional[str] = None 