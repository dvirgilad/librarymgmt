"""DB models for patrons"""
from mongoengine import Document, StringField, IntField, FloatField, ReferenceField
from library.library_model import LibraryModel


class PatronModel(Document):
    """Patron model for DB"""

    name = StringField(required=True)
    category = StringField()
    fines = IntField(0)
    discount = FloatField(0.0)
    library = ReferenceField(LibraryModel)

    meta = {"allow_inheritance": True}


class StudentModel(PatronModel):
    """Student model for DB"""

    degree = StringField()


class TeacherModel(PatronModel):
    """Teacher model for DB"""

    subject = StringField()
