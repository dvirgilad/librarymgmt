"""DB models for library items"""
from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField
from patrons.patron_model import PatronModel
from library.library_model import LibraryModel


class LibraryItemModel(Document):
    """Library item model for DB"""

    name = StringField(required=True)
    genre = StringField()
    fine = IntField(0)
    borrowing_period = IntField(0)
    borrowed_status = BooleanField()
    borrower = ReferenceField(PatronModel)
    library = ReferenceField(LibraryModel)
    meta = {"allow_inheritance": True}


class BookModel(LibraryItemModel):
    """Student model for DB"""

    author = StringField()


class DiskModel(LibraryItemModel):
    """Teacher model for DB"""

    band = StringField()
