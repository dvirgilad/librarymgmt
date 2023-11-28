from datetime import datetime
import random
from patrons import Patron

import time


class Item:
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

    def match_string(self):
        pass


class Book(Item):
    def __init__(
        self,
        name: str,
        author: str,
        genre: str,
    ):
        super().__init__(name, "book")
        self.author, self.genre = author, genre
        self.serial = random.randint(1, 1000)

    def match_string(self, query):
        if (
            query.lower() in self.name.lower()
            or query.lower() in self.author.lower()
            or query.lower() in str(self.serial)
            or query.lower() in self.genre
        ):
            return True
        return False


class Disk(Item):
    def __init__(self, name: str, band: str, genre: str):
        super().__init__(name, "disk")
        self.band, self.genre = band, genre
        self.serial = random.randint(1001, 1999)

    def match_string(self, query):
        if (
            query.lower() in self.name.lower()
            or query.lower() in self.band.lower()
            or query.lower() in str(self.serial)
            or query.lower() in self.genre
        ):
            return True
        return False
