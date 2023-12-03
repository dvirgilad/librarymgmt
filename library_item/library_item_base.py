"""Base Library Item """
import abc
from patrons.patron_base import Patron, ProtectedAttribute


class DeleteBorrowingPeriodError(Exception):
    """Error if user tries to delete the borrowing period"""


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

    @property
    def borrower(self):
        """Patron currently borrowing this item. None if not being borrowed"""
        return self._borrower

    @property
    def borrowing_period(self):
        """Borrowing period property"""
        return self._borrowing_period

    @borrowing_period.setter
    def borrowing_period(self, new_value):
        self._borrowing_period = new_value

    @borrowing_period.deleter
    def borrowing_period(self):
        raise DeleteBorrowingPeriodError("Cannot Delete Borrowing Period")

    @property
    def fine(self):
        """Fine for late returns property"""
        return self._borrowing_period

    @fine.setter
    def fine(self, new_value):
        self._borrowing_period = new_value

    @fine.deleter
    def fine(self):
        self._borrowing_period = 0

    def change_borrower(self, borrower: Patron = None):
        """Change borrrower or set to None if book is returned"""
        if self._borrower and borrower:
            raise ProtectedAttribute("Item must be returned first")
        self._borrower = borrower

    def update_item(self, attribute_to_edit: str, new_value: str) -> None:
        """Change valid attributes of a library item"""
        for item_attribute in vars(self).keys():
            if item_attribute.lower() == attribute_to_edit.lower():
                setattr(self, item_attribute, new_value)
                return
        raise AttributeError

    def match_string(self, query) -> bool:
        """Check if query string matches any attribute of item for search"""
        for value in vars(self).values():
            if query.lower() in str(value).lower():
                return True
        return False
