from datetime import datetime
import random
import abc
from patrons.patron_base import Patron


class LibraryItem(abc.ABC):
    def __init__(
        self,
        name,
        item_type,
        fine,
        borrowing_period,
    ):
        self.name, self.type, self.fine, self.borrowing_period, self.borrowed_status = (
            name,
            item_type,
            fine,
            borrowing_period,
            False,
        )

    def borrow(self, borrower: Patron):
        if self.borrowed_status:
            print(f"This {self.type} is currently checked out!")
            return False
        else:
            self.time_borrowed = datetime.now()
            self.borrower = borrower
            self.borrowed_status = True
            print(f"{borrower.name} checked out {self.name}")
            return True

    def unborrow(self):
        time_returned = datetime.now()
        time_borrowed = (time_returned - self.time_borrowed).microseconds
        print(time_borrowed)
        if time_borrowed > self.borrowing_period:
            fine = self.fine * (time_borrowed - self.borrowing_period)
            print(
                f"{self.borrower.name} has returned this {self.type} late and for that {self.borrower.name} must pay a ${fine} fine!"
            )
            self.borrower.fines += fine
        self.borrower = None
        self.borrowed_status = False
        print(f"{self.name} returned")
        return True

    def update(self, field: str, value):
        if hasattr(self, field):
            setattr(self, field, value)

    def match_string(self, query):
        for property, value in vars(self).items():
            if query.lower() in str(value).lower():
                return True
