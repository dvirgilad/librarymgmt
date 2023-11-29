from datetime import datetime
import random
import abc
from patrons.patron_base import Patron



class LibraryItem(abc.ABC):
    def __init__(self, name, type):
        self.name, self.type = name, type

    def borrow(self, borrower: Patron):
        if hasattr(self, "borrower"):
            print(f"This {self.type} is currently checked out!")
        else:
            self.borrowed = datetime.now()
            self.borrower = borrower
            print(f"{borrower.name} checked out {self.name}")

    def unborrow(self):
        time_borrowed = (datetime.now() - self.borrowed).microseconds
        print(time_borrowed)
        if time_borrowed > 30:
            fine = 500 * time_borrowed - 30
            print(
                f"{self.borrower.name} has returned this {self.type} late and for that you must pay a ${fine} fine!"
            )
            self.borrower.fines += fine
        delattr(self, "borrower")
        delattr(self, "borrowed")
        print(f"{self.name} returned")

    def update(self, field: str, value):
        if hasattr(self, field):
            setattr(self, field, value)

    @abc.abstractmethod
    def match_string(self):
        pass



