"""Base Patron class"""
import abc
from enum import Enum
from patrons.patron_model import StudentModel, TeacherModel


class PatronTypes(Enum):
    """Enum for types of patrons"""

    STUDENT = StudentModel
    TEACHER = TeacherModel


class Patron(abc.ABC):
    """Base patron class: accepts name, category(student/teacher/...) and a fine discount"""

    def __init__(self, name: str, category: str, fine_discount: int):
        self.name, self._category, self._fines, self.fine_discount = (
            name,
            category,
            0,
            fine_discount,
        )
