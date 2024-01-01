"""DB models for library items"""
from typing import Literal
from beanie import Document
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from patrons.dal.patron_model import PatronModel
from pymongo import TEXT


class LibraryItemCreate(BaseModel):
    name: str
    genre: str
    fine: int
    borrowing_period: int
    category: Literal["DISK", "BOOK"]
    library_item_attributes: dict = {}


class LibraryItemReturn(LibraryItemCreate):
    borrowed_status: bool = False
    borrower: str | None = None
    borrowed_at: datetime | None = None
    id: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class LibraryItemEdit(BaseModel):
    name: str = None
    genre: str = None
    fine: int = None
    borrowing_period: int = None
    library_item_attributes: dict = None


class LibraryItemModel(Document, LibraryItemCreate):
    borrower: PatronModel | None = None
    borrowed_at: datetime | None = None
    borrowed_status: bool = False

    class Settings:
        indexes = [[("name", TEXT), ("genre", TEXT)]]
