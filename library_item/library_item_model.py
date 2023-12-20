"""DB models for library items"""
from typing import Annotated, Union, Literal
from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ReferenceField,
    DateTimeField,
    DynamicDocument,
    DictField,
)
from bson import ObjectId
from patrons.patron_model import PatronModel, PyObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from datetime import datetime


def borrower_to_string(v: any):
    if v is None:
        return v
    if isinstance(v, ObjectId):
        return str(v)
    return None


class LibraryItemModel(DynamicDocument):
    """Library item model for DB"""

    name = StringField(required=True)
    genre = StringField()
    fine = IntField(0)
    category = StringField()
    borrowing_period = IntField(0)
    borrowed_status = BooleanField(default=False)
    borrower = ReferenceField(PatronModel)
    borrowed_at = DateTimeField(default=None)
    library_item_attributes = DictField()
    meta = {
        "indexes": [
            {
                "name": "text_index",
                "fields": ["$name", "$genre"],
                "default_language": "none",
                "weights": {"name": 5, "genre": 4},
            }
        ],
    }


class LibraryItemBase(BaseModel):
    name: str
    genre: str
    fine: int
    borrowing_period: int
    category: Literal["DISK", "BOOK"]
    library_item_attributes: dict = {}


class LibraryItem(LibraryItemBase):
    borrowed_status: bool = False
    borrower: Annotated[Union[str, None], BeforeValidator(borrower_to_string)] = None
    borrowed_at: datetime | None = None
    id: PyObjectId = Field(alias="_id", default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)
