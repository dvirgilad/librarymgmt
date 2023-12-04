"""DB models for patrons"""
from mongoengine import Document, StringField, IntField, FloatField


class PatronModel(Document):
    """Patron model for DB"""

    name = StringField(required=True)
    category = StringField()
    fines = IntField(0)
    discount = FloatField(0.0)
    meta = {"allow_inheritance": True}


class StudentModel(PatronModel):
    """Student model for DB"""

    degree = StringField()


class TeacherModel(PatronModel):
    """Teacher model for DB"""

    subject = StringField()
