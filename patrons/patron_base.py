"""Base Patron class"""
import abc
from enum import Enum


class ProtectedAttribute(Exception):
    """If editing protected attribute"""


class PatronTypes(Enum):
    """Enum for types of patrons"""

    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class Patron(abc.ABC):
    """Base patron class: accepts name, category(student/teacher/...) and a fine discount"""

    def __init__(self, name: str, category: str, fine_discount: int):
        self.name, self._category, self._fines, self.fine_discount = (
            name,
            category,
            0,
            fine_discount,
        )

    @property
    def category(self):
        """Patron category attribute"""
        return self._category

    @category.setter
    def category(self):
        raise AttributeError

    @property
    def fines(self):
        """fines accrued by a patron"""
        return self._fines

    @fines.getter
    def fines(self):
        """return fine amount with discount"""
        return self._fines

    @fines.setter
    def fines(self, new_value):
        raise ProtectedAttribute("You are not allowed to change fines!")

    @fines.deleter
    def fines(self):
        raise ProtectedAttribute("You are not allowed to change fines!")

    def add_fine(self, new_amount: int) -> None:
        """Add fines to a patron"""
        self._fines += new_amount * self.fine_discount
