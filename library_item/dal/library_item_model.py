"""DB models for library items"""
from typing import Literal

from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
