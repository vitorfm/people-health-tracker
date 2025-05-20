from .person import Person
from pydantic import Field

class Doctor(Person):
    specialty: str = Field(...) 