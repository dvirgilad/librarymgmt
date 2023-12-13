"""DB models for patrons"""
from mongoengine import Document, StringField, IntField, FloatField
from pydantic import BaseModel


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


class PatronBase(BaseModel):
    """Base patron object"""

    name: str
    fine_discount: float
    fines: float


class StudentBase(PatronBase):
    """base student object"""

    category: str = "STUDENT"
    degree: str


class TeacherBase(PatronBase):
    """base teacher object"""

    category: str = "TEACHER"
    subject: str
