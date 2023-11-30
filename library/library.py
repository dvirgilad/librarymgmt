"""Library Class. Handles Patrons and library items"""
from datetime import datetime
from library_item.library_item_base import LibraryItem
from patrons.patron_base import Patron
import csv


class Library:
    """Library class: accepts, name, list of patrons and dict of items with their ids"""

    def __init__(self, name, patrons: [Patron], library_items: dict = None):
        self.name, self.patrons = name, patrons
        self.library_items = library_items if library_items else {}

    def show_members(self) -> None:
        """Prints all patrons of the library"""
        for member in self.patrons:
            print(f"{member.name}:\t{member.category} ")

    def show_catalog(self) -> None:
        """Prints all library Items"""
        for library_item in self.library_items.values():
            print(
                f"{library_item.name}\t\t\t {library_item.type}\t\t\t {library_item.genre}"
            )

    def add_item(self, library_item: LibraryItem) -> bool:
        """Add one item to library"""
        self.library_items[id(library_item)] = library_item
        print(f"added {library_item.name}")
        return True

    def add_items(self, library_item_list: [LibraryItem]) -> bool:
        """Add multiple items as an array to library"""
        for library_item in library_item_list:
            self.add_item(library_item)
        return True

    def remove_item(self, item_to_remove: LibraryItem) -> bool:
        """remove one item from library"""
        try:
            del self.library_items[id(item_to_remove)]
            print(f"{item_to_remove} removed")
            return True
        except KeyError:
            print("book not found")
            return False

    def add_patron(self, member: Patron) -> bool:
        """Add one patron to the library"""
        self.patrons.append(member)
        print(f"{member.name} has joined the Library")
        return True

    def add_patrons(self, patron_list: [Patron]) -> bool:
        """Add multiple patrons as an array to the Library"""
        for patron in patron_list:
            self.patrons.append(patron)
            print(f"{patron.name} has joined the Library")
        return True

    def remove_patron(self, patron_name: str) -> bool:
        """Remove one patron from the library"""
        for patron in self.patrons:
            if patron.name.lower() == patron_name.lower():
                self.patrons.remove(patron)
                return True
        return False

    def search_library(self, query: str) -> [LibraryItem]:
        """Search all items in the library to match a string"""
        result = []
        for library_item in self.library_items.values():
            if library_item.match_string(query):
                result.append(library_item)
                print(library_item.name)
        return result

    def borrow_item(self, item_to_borrow: LibraryItem, borrower: Patron) -> bool:
        """Checks if Item is borrowed and if patron is part of library. Then borrows book"""
        if item_to_borrow.borrowed_status:
            print(f"This {item_to_borrow.type} is currently checked out!")
            return False
        if borrower not in self.patrons:
            print(f"{borrower.name} not a registerd Patron")
            return False
        item_to_borrow.time_borrowed = datetime.now()
        item_to_borrow.borrower = borrower
        item_to_borrow.borrowed_status = True
        self.record_transaction(item_to_borrow, borrower)
        print(f"{borrower.name} checked out {item_to_borrow.name}")
        return True

    def record_transaction(self, library_item: LibraryItem, patron: Patron):
        """Write Library transaction to transaction.csv"""
        action = "RETURNED"
        if library_item.borrowed_status:
            action = "BORROWED"
        with open("transactions.csv", "a", newline="", encoding="UTF-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(
                [
                    str(library_item.time_borrowed),
                    patron.name,
                    action,
                    library_item.name,
                ]
            )
            return True

    def return_item(self, item_to_return: LibraryItem) -> bool:
        """Return library item to library."""
        time_returned = datetime.now()
        time_borrowed = (time_returned - item_to_return.time_borrowed).microseconds
        print(time_borrowed)
        if time_borrowed > item_to_return.borrowing_period:
            fine = item_to_return.fine * (
                time_borrowed - item_to_return.borrowing_period
            )

            print(
                f"{item_to_return.borrower.name} has returned this {item_to_return.type}"
                f" late and for that {item_to_return.borrower.name} must pay a ${fine} fine!"
            )
            item_to_return.borrower.fines += fine
        item_to_return.borrowed_status = False
        self.record_transaction(item_to_return, item_to_return.borrower)
        item_to_return.borrower = None
        print(f"{item_to_return.name} returned")
        return True
