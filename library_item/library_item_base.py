"""Base Library Item """
import abc


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
        ) = (
            name,
            item_type,
            fine,
            borrowing_period,
            False,
        )

    @property
    def borrowing_period(self):
        """Borrowing period property"""
        return self._borrowing_period

    @borrowing_period.setter
    def borrowing_period(self, new_value):
        self._borrowing_period = new_value

    @borrowing_period.deleter
    def borrowing_period(self):
        raise DeleteBorrowingPeriodError("Cannot Delete Borrowing")

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

    def update_item(self, attribute_to_edit: str, new_value: str) -> bool:
        """Change valid attributes of a library item"""
        for item_attribute in vars(self).keys():
            if item_attribute.lower() == attribute_to_edit.lower():
                setattr(self, item_attribute, new_value)
                return True
        return False

    def match_string(self, query) -> bool:
        """Check if query string matches any attribute of item for search"""
        for value in vars(self).values():
            if query.lower() in str(value).lower():
                return True
        return False
