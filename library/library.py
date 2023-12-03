"""Library Class. Handles Patrons and library items"""
from datetime import datetime
from library_item.library_item_base import LibraryItem
from patrons.patron_base import Patron
from transactions.transactions import Transaction, Actions


class DeleteAttributeException(Exception):
    """Exception raised if there is an attempt to delete a protected attribute"""


class PatronNotFound(Exception):
    """Exception raised if patron not found in library"""


class LibraryItemNotFound(Exception):
    """Exception raised if library item not found in library"""


class Library:
    """Library class: accepts, name, list of patrons and dict of items with their ids"""

    def __init__(self, name, patrons: [Patron], library_items: dict = None):
        self.name, self._patrons = name, patrons
        self._library_items = library_items if library_items else {}

    @property
    def library_items(self):
        """library items attribute"""
        return self._library_items

    @property
    def patrons(self):
        """Base patrons category"""
        return self._patrons

    @patrons.getter
    def patrons(self):
        """returns a dict with every patron as {name: category}"""
        patron_dict = {}
        for patron in self._patrons:
            patron_dict[patron.name] = patron.category
        return patron_dict

    @patrons.deleter
    def patrons(self):
        raise DeleteAttributeException("You are not allowed to delete the patron list!")

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

    def remove_item(self, item_to_remove: LibraryItem) -> None:
        """remove one item from library"""
        try:
            del self.library_items[id(item_to_remove)]
            print(f"{item_to_remove} removed")
        except KeyError as err:
            raise LibraryItemNotFound from err

    def add_patron(self, member: Patron) -> bool:
        """Add one patron to the library"""
        self._patrons.append(member)
        print(f"{member.name} has joined the Library")
        return True

    def add_patrons(self, patron_list: [Patron]) -> bool:
        """Add multiple patrons as an array to the Library"""
        for patron in patron_list:
            self._patrons.append(patron)
            print(f"{patron.name} has joined the Library")
        return True

    def remove_patron(self, patron_name: str) -> None:
        """Remove one patron from the library"""
        for patron in self._patrons:
            if patron.name.lower() == patron_name.lower():
                self._patrons.remove(patron)
                return
        raise PatronNotFound(f"{patron_name} not found in {self.name}")

    def search_library(self, query: str) -> [LibraryItem]:
        """Search all items in the library to match a string"""
        result = []
        for library_item in self.library_items.values():
            if library_item.match_string(query):
                result.append(library_item)
        if len(result) == 0:
            raise LibraryItemNotFound(f"No item in library matches {query}")
        return result

    def borrow_item(self, item_to_borrow: LibraryItem, borrower: Patron) -> bool:
        """Checks if Item is borrowed and if patron is part of library. Then borrows book"""
        if item_to_borrow.borrowed_status:
            print(f"This {item_to_borrow.type} is currently checked out!")
            return False
        if borrower.name not in self.patrons:
            print(f"{borrower.name} not a registerd Patron")
            return False
        item_to_borrow.time_borrowed = datetime.now()
        item_to_borrow.change_borrower(borrower)
        item_to_borrow.borrowed_status = True
        Transaction(
            borrower.name,
            item_to_borrow.name,
            Actions.BORROWED.value,
            item_to_borrow.time_borrowed,
        ).send_to_csv()
        print(f"{borrower.name} checked out {item_to_borrow.name}")
        return True

    def return_item(self, item_to_return: LibraryItem) -> None:
        """Return library item to library."""
        time_returned = datetime.now()
        time_borrowed = (time_returned - item_to_return.time_borrowed).microseconds
        if time_borrowed > item_to_return.borrowing_period:
            fine = item_to_return.fine * (
                time_borrowed - item_to_return.borrowing_period
            )

            print(
                f"{item_to_return.borrower.name} has returned this {item_to_return.type}"
                f" late and for that {item_to_return.borrower.name} must pay a ${fine} fine!"
            )
            item_to_return.borrower.add_fine(fine)
        item_to_return.borrowed_status = False
        item_to_return.time_borrowed = None
        Transaction(
            item_to_return.borrower.name,
            item_to_return.name,
            Actions.RETURNED.value,
            datetime.now(),
        ).send_to_csv()
        item_to_return.change_borrower()
        print(f"{item_to_return.name} returned")
