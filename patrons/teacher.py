from patrons.patron_base import Patron

class Teacher(Patron):
    def __init__(self, name: str, subject: str):
        super().__init__("teacher")
        self.name, self.subject = name, subject

    def get_fines(self):
        print('Employee Discount:')
        print(f"{self.name} has to pay ${self.fines * 0.5} in FINES")
