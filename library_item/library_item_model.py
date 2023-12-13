"""DB models for library items"""
from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ReferenceField,
    DateField,
)
from patrons.patron_model import PatronModel
from pydantic import BaseModel
from datetime import datetime


class LibraryItemModel(Document):
    """Library item model for DB"""

    name = StringField(required=True)
    genre = StringField()
    fine = IntField(0)
    category = StringField()
    borrowing_period = IntField(0)
    borrowed_status = BooleanField(default=False)
    borrower = ReferenceField(PatronModel)
    borrowed_at = DateField(None)
    meta = {"allow_inheritance": True, "fields": ["$name", "$genre", "$band", "$genre"]}


class BookModel(LibraryItemModel):
    """Student model for DB"""

    author = StringField()


class DiskModel(LibraryItemModel):
    """Teacher model for DB"""

    band = StringField()


class LibraryItemBase(BaseModel):
    """Library item basemodel"""

    name: str
    genre: str
    fine: int
    borrowing_period: int
    borrowed_status: bool = False
    borrower: str = None
    borrowed_at: datetime | None = None


class BookBase(LibraryItemBase):
    category: str = "BOOK"
    author: str


class DiskBase(LibraryItemBase):
    category: str = "DISK"
    band: str
