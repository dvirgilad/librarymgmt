from patrons.patron_base import Patron

class Student(Patron):
    def __init__(self, name: str, degree: str):
        super().__init__("student")
        self.name, self.degree = name, degree

    def get_fines(self):
        print('Student Discount:')
        print(f"{self.name} has to pay ${self.fines * 0.8} in FINES")
