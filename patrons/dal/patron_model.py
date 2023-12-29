"""DB models for patrons"""
from typing import Literal
from pydantic import BaseModel


class PatronCreate(BaseModel):
    """Input class for patron"""

    name: str
    fine_discount: float
    fines: float
    category: Literal["TEACHER", "STUDENT"]
    patron_attributes: dict = {}


class PatronReturn(PatronCreate):
    """Base patron object"""

    id: str


class PatronEdit(BaseModel):
    """Patron class with attributes that can be edited"""

    name: str = None
    fine_discount: str = None
    patron_attributes: dict = None
