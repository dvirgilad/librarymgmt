"""Library Class. Handles Patrons and library items"""
from datetime import datetime
from patrons.patron_model import PatronModel
from library_item.library_item_base import LibraryItem
from patrons.patron_base import Patron
from transactions.transactions import Transaction, Actions
from library.library_model import LibraryModel
from library_item.library_item_model import LibraryItemModel


class DeleteAttributeException(Exception):
    """Exception raised if there is an attempt to delete a protected attribute"""


class PatronNotFound(Exception):
    """Exception raised if patron not found in library"""


class LibraryItemNotFound(Exception):
    """Exception raised if library item not found in library"""


class Library:
    """Library class: accepts, name, list of patrons and dict of items with their ids"""

    def __init__(self, name, patrons: [Patron], library_items: dict = None):
        self.name, self._patrons = name, []
        self._library_items = library_items if library_items else {}
        self.db_model = LibraryModel(name=name).save()
        for patron in patrons if patrons else []:
            self.add_patron(patron)
        for library_item in self._library_items.values():
            self.add_item(library_item)

    @property
    def library_items(self):
        """library items attribute"""
        return self._library_items

    @library_items.getter
    def library_items(self):
        """return array of library items"""
        library_items = []
        for library_item in LibraryItemModel.objects(library=self.db_model):
            library_items.append(library_item)
        return library_items

    @library_items.setter
    def library_items(self):
        """return array of library items"""
        raise DeleteAttributeException("Cannot edit library items")

    @property
    def patrons(self):
        """Base patrons category"""
        return self._patrons

    @patrons.getter
    def patrons(self):
        """returns a dict with every patron as {name: category}"""
        patron_dict = {}

        for patron in PatronModel.objects(library=self.db_model):
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

    def add_item(self, library_item: LibraryItem) -> None:
        """Add one item to library"""
        library_item.db_model.library = self.db_model
        library_item.db_model.save()

    def add_items(self, library_item_list: [LibraryItem]) -> bool:
        """Add multiple items as an array to library"""
        for library_item in library_item_list:
            self.add_item(library_item)
        return True

    def remove_item(self, item_to_remove: LibraryItem) -> None:
        """remove one item from library"""
        try:
            del self._library_items[id(item_to_remove)]
            item_to_remove.db_model.delete()
        except KeyError as err:
            raise LibraryItemNotFound from err

    def add_patron(self, member: Patron) -> None:
        """Add one patron to the library"""
        member.db_model.library = self.db_model
        member.db_model.save()

    def add_patrons(self, patron_list: [Patron]) -> bool:
        """Add multiple patrons as an array to the Library"""
        for patron in patron_list:
            self.add_patron(patron)

        return True

    def remove_patron(self, patron_name: str) -> None:
        """Remove one patron from the library"""

        remove_patron = PatronModel.objects(
            name=patron_name, library=self.db_model
        ).delete()
        if remove_patron == 0:
            raise PatronNotFound(f"{patron_name} not found in {self.name}")

    def search_library(self, query: str) -> [LibraryItem]:
        """Search all items in the library to match a string"""
        result = []
        for library_item in self._library_items.values():
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
            raise PatronNotFound(f"Patron {borrower.name} not a member of {self.name}")
        item_to_borrow.time_borrowed = datetime.now()
        item_to_borrow.change_borrower(borrower)
        item_to_borrow.borrowed_status = True
        # Transaction(
        #     borrower.name,
        #     item_to_borrow.name,
        #     Actions.BORROWED.value,
        #     item_to_borrow.time_borrowed,
        # ).send_to_csv()
        Transaction(
            borrower,
            item_to_borrow,
            Actions.BORROWED.value,
            item_to_borrow.time_borrowed,
        ).send_to_mongo()
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
        # Transaction(
        #     item_to_return.borrower.name,
        #     item_to_return.name,
        #     Actions.RETURNED.value,
        #     datetime.now(),
        # ).send_to_csv()
        Transaction(
            item_to_return.borrower,
            item_to_return,
            Actions.RETURNED.value,
            datetime.now(),
        ).send_to_mongo()
        item_to_return.change_borrower()
        print(f"{item_to_return.name} returned")
