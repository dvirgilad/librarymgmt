"""DB models for library items"""
from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ReferenceField,
    DateTimeField,
    DynamicDocument,
)
from patrons.patron_model import PatronModel, PyObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from datetime import datetime
from typing import Annotated, Union
from bson import ObjectId


def borrower_to_string(v: any):
    if v is None:
        return v
    if isinstance(v, ObjectId):
        return str(v)
    return None


class LibraryItemModel(DynamicDocument):
    """Library item model for DB"""

    name = StringField(required=True, index=True)
    genre = StringField(index=True)
    fine = IntField(0)
    category = StringField(index=True)
    borrowing_period = IntField(0)
    borrowed_status = BooleanField(default=False)
    borrower = ReferenceField(PatronModel)
    borrowed_at = DateTimeField(default=None)
    meta = {"allow_inheritance": True}


class BookModel(LibraryItemModel):
    """Student model for DB"""

    author = StringField(index=True)


class DiskModel(LibraryItemModel):
    """Teacher model for DB"""

    band = StringField(index=True)


class LibraryItem(BaseModel):
    name: str
    genre: str
    fine: int
    borrowing_period: int
    borrowed_status: bool = False
    borrower: Annotated[Union[str, None], BeforeValidator(borrower_to_string)] = None
    borrowed_at: datetime | None = None


class Book(LibraryItem):
    category: str = "BOOK"
    author: str


class Disk(LibraryItem):
    category: str = "DISK"
    band: str


class LibraryItemBase(BaseModel):
    """Library item basemodel"""

    id: PyObjectId = Field(alias="_id", default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BookBase(LibraryItemBase, Book):
    pass


class DiskBase(LibraryItemBase, Disk):
    pass
