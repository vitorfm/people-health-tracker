from typing import Any

from bson import ObjectId
from pydantic_core import core_schema

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        # Deprecated in Pydantic V2, but kept for potential compatibility or as a fallback
        yield cls.validate_objectid

    @classmethod
    def validate_objectid(cls, v: Any, info: core_schema.ValidationInfo) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        # This method is used by Pydantic V2 for schema generation and validation
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate_objectid),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x)),
        ) 