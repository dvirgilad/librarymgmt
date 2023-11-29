from patrons.patron_base import Patron


class Teacher(Patron):
    def __init__(self, name: str, subject: str):
        super().__init__("teacher", fine_discount=0.5)
        self.name, self.subject = name, subject
