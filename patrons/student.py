"""Student Class - inherits from the base Patron class"""
from patrons.patron_base import Patron


class Student(Patron):
    """Student class: Accepts a name and degree. The fine discount is 150%"""

    def __init__(self, name: str, degree: str):
        super().__init__(name, "student", fine_discount=1.5)
        self.degree = degree
