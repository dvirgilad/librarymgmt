"""Base Library Item """
import abc
from patrons.patron_base import Patron
from patrons.patron_controller import ProtectedAttribute
from enum import Enum


class DeleteBorrowingPeriodError(Exception):
    """Error if user tries to delete the borrowing period"""


class LibraryItemTypes(Enum):
    """Enum for types of patrons"""

    DISK = "DISK"
    BOOK = "BOOK"


class LibraryItem(abc.ABC):
    """Base Library Class: accepts name, item type fine and borrowing period"""

    def __init__(
        self,
        name,
        item_type,
        fine,
        borrowing_period,
    ):
        (
            self.name,
            self.type,
            self._fine,
            self._borrowing_period,
            self.borrowed_status,
            self._borrower,
            self.time_borrowed,
        ) = (name, item_type, fine, borrowing_period, False, None, None)
