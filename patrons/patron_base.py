"""Base Patron class"""
import abc


class LoweringFinesException(Exception):
    """If setting a lower fine ammount"""


class Patron(abc.ABC):
    """Base patron class: accepts name, category(student/teacher/...) and a fine discount"""

    def __init__(self, name: str, category: str, fine_discount: int):
        self.name, self.category, self._fines, self.fine_discount = (
            name,
            category,
            0,
            fine_discount,
        )

    @property
    def fines(self):
        """fines accrued by a patron"""
        return self._fines

    @fines.getter
    def fines(self):
        """return fine amount with discount"""
        return self._fines * self.fine_discount

    @fines.setter
    def fines(self, new_value):
        raise LoweringFinesException("You are not allowed to lower the fine amount!")

    @fines.deleter
    def fines(self):
        raise LoweringFinesException("You are not allowed to lower fines!")

    def update_patron(self, field: str, value) -> None:
        """Updates the valid fields of a patron"""

        if hasattr(self, field.lower()) and field.lower() != "items":
            setattr(self, field.lower(), value)
        raise AttributeError(f"{field} attribute not found")
