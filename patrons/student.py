"""Student Class - inherits from the base Patron class"""
from patrons.patron_base import Patron, PatronTypes
from patrons.patron_model import StudentModel


class Student(Patron):
    """Student class: Accepts a name and degree. The fine discount is 150%"""

    def __init__(self, name: str, degree: str):
        student_fine_discount = 1.5
        super().__init__(
            name, PatronTypes.STUDENT.name, fine_discount=student_fine_discount
        )
        self.degree = degree
