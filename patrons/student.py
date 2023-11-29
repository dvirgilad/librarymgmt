from patrons.patron_base import Patron


class Student(Patron):
    def __init__(self, name: str, degree: str):
        super().__init__("student", fine_discount=1.5)
        self.name, self.degree = name, degree
