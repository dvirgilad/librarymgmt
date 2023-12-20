"""DB models for patrons"""
from mongoengine import Document, StringField, IntField, FloatField
from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    AfterValidator,
    WithJsonSchema,
    ConfigDict,
)
from bson import ObjectId
from pydantic_core import core_schema
from typing import Annotated, Any, Union
from pydantic.json_schema import JsonSchemaValue


def validate_object_id(v: Any) -> ObjectId:
    """validator for mongo objectID field

    Args:
        v (Any): objectid attribute

    Raises:
        ValueError: if v is not an objectID field

    Returns:
        ObjectId: Mongo objectID
    """
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v) and ObjectId is not None:
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class PatronModel(Document):
    """Patron model for DB"""

    name = StringField(required=True)
    category = StringField()
    fines = IntField(0)
    fine_discount = FloatField(0.0)

    meta = {"allow_inheritance": True}


class StudentModel(PatronModel):
    """Student model for DB"""

    degree = StringField()


class TeacherModel(PatronModel):
    """Teacher model for DB"""

    subject = StringField()


class Patron(BaseModel):
    """class all patrons inherit from"""

    name: str
    fine_discount: float
    fines: float


class Teacher(Patron):
    category: str = "TEACHER"
    subject: str


class Student(Patron):
    category: str = "STUDENT"
    degree: str


class PatronBase(Patron):
    """Base patron object"""

    id: PyObjectId = Field(alias="_id", default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class StudentBase(PatronBase, Student):
    """base student object"""


class TeacherBase(PatronBase, Teacher):
    """base teacher object"""
