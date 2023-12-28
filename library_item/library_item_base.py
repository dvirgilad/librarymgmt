"""Base Library Item """
from enum import Enum


class DeleteBorrowingPeriodError(Exception):
    """Error if user tries to delete the borrowing period"""


class LibraryItemTypes(Enum):
    """Enum for types of patrons"""

    DISK = "DISK"
    BOOK = "BOOK"
