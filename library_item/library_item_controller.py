""" Bussiness logic layer for library items """
from datetime import datetime
from library_item.library_item_model import (
    LibraryItemModel,
    LibraryItemBase,
    LibraryItem,
)
from library.library_dal import add_to_db, remove_from_db
from library.library_exceptions import ProtectedAttribute
from library_item.library_item_dal import (
    get_all_library_items_from_db,
    get_library_item_from_db,
    update_libray_items_info_in_db,
    search_library_items_in_db,
)
from patrons.patron_controller import search_for_patron
from patrons.dal.patron_dal import update_patron_info_in_db
from transactions.transactions import Transaction, Actions


class InvalidLibraryItem(Exception):
    """Exception raise if library item is invalid"""


class LibraryItemNotFound(Exception):
    """Exception raised if library item not found in library"""


class LibraryItemModelFactory:
    """Patron model factory class"""

    def create_model(self, library_item: LibraryItemBase) -> LibraryItemModel:
        """creates library_item document model from basemodel

        Args:
            patron (LibraryItemBase): library_item basemodel

        Returns:
            _type_: library_item document model
        """

        db_model = LibraryItemModel(**library_item.model_dump())
        return db_model

    def create_basemodel(self, library_item_model: LibraryItemModel) -> LibraryItem:
        """generates library item basemodel from document model

        Args:
            patron_model (PatronModel): patron document model

        Returns:
            LibraryItem: patron basemodel
        """
        library_item_basemodel = LibraryItem(
            **library_item_model.to_mongo().to_dict())
        return library_item_basemodel


def create_library_item(library_item: LibraryItemBase) -> str:
    """adds library item to db and returns its mongo ID

    Args:
        library_item (LibraryItem): Library item basemodel

    Returns:
        str: library items mongo ID
    """

    db_model = LibraryItemModelFactory().create_model(library_item=library_item)
    item_id = add_to_db(db_model)
    return str(item_id)


def search_for_library_item_by_id(item_id: str) -> LibraryItemModel:
    """search for library item in DB. raise LibraryItemNotFound if not found

    Args:
        patron_id (str): library item mongo id

    Raises:
        LibraryItemNotFound: raised if no library item with given id is found

    Returns:
        LibraryItemModel: library item document model
    """
    patron_db_model = get_library_item_from_db(item_id)
    if patron_db_model is None:
        raise LibraryItemNotFound(
            f"Library item with ID: {item_id} not found in DB")
    return patron_db_model


def remove_library_item(item_id: str) -> None:
    """Checks if library item exists in db and deletes it
    Args:
        item_id (str): Item mongo id
    Raises:
        InvalidLibraryItem: raised if library item cannot be deleted
    """
    library_item_model = search_for_library_item_by_id(item_id)
    if check_if_borrowed(library_item_model):
        raise InvalidLibraryItem(
            "Cannot delete an item that is currently checked out")
    remove_from_db(library_item_model)


def update_library_item(item_id: str, attribute: str, new_value: str) -> None:
    """updates the given attribute of a library item

    Args:
        item_id (str): ID of item to update
        attribute (str): attribute of item to update
        new_value (str): new value of given attribute
    """

    if attribute.upper() in ["BORROWER", "BORROWED_STATUS", "BORROWED_AT"]:
        raise ProtectedAttribute(f"Cannot edit an items {attribute}")
    patron_model = search_for_library_item_by_id(item_id)
    update_libray_items_info_in_db(patron_model, attribute, new_value)


def get_library_item(item_id: str) -> LibraryItem:
    """searches for library item and returns its basemodel

    Args:
        item_id (str): item mongo ID

    Returns:
        LibraryItem: Item basemodel
    """
    item_model = search_for_library_item_by_id(item_id=item_id)
    item_basemodel = LibraryItemModelFactory().create_basemodel(item_model)
    return item_basemodel


def check_if_borrowed(library_item: LibraryItemModel) -> bool:
    """check if library item is currently checked out

    Args:
        library_item (LibraryItemModel): Library item to check

    Returns:
        bool: if borrowed or not
    """
    if (
        library_item.borrowed_status
        or library_item.borrower is not None
        or library_item.borrowed_at is not None
    ):
        return True
    return False


def borrow_item(item_id: str, borrower_id: str) -> str:
    """Borrows an item by a patron and logs it in the transactions table

    Args:
        item_id (str): ID of item to borrow
        borrower_id (str): ID of patron that is borrowing
    Raises:
        InvalidLibraryItem: raised if library item cannot be borrowed
    Returns:
        str: mongo id of transaction
    """
    patron_model = search_for_patron(borrower_id)
    item_model = search_for_library_item_by_id(item_id)
    time_borrowed = datetime.utcnow()
    if check_if_borrowed(item_model):
        raise InvalidLibraryItem(
            f"Item with ID {item_id} is already borrowed!")
    update_libray_items_info_in_db(
        item_model,
        **{
            "borrower": patron_model,
            "borrowed_status": True,
            "borrowed_at": time_borrowed,
        },
    )
    transaction_id = Transaction(
        patron=patron_model,
        library_item=item_model,
        action=Actions.BORROWED.value,
        timestamp=time_borrowed,
    ).send_log_to_db()
    return transaction_id


def check_if_returned_late(
    library_item: LibraryItemModel, time_returned: datetime
) -> int:
    """check if library item is returned late. returns the amount of fines to add to patron

    Args:
        library_item (LibraryItemModel): item being returned
        time_returned (datetime): timestamp of when item is returned

    Returns:
        int: amount of fines to add
    """

    time_difference = (time_returned - library_item.borrowed_at).seconds
    if time_difference > library_item.borrowing_period:
        return time_difference * library_item.fine
    return 0


def return_library_item(item_id: str) -> str:
    """Returns an item to the library

    Args:
        item_id (str): mongo id of library id
    Raises:
        InvalidLibraryItem: raised if library item is not checked out
    Returns:
        str: mongo id of transaction
    """
    item_model = search_for_library_item_by_id(item_id)
    patron_model = item_model.borrower
    time_returned = datetime.utcnow()
    if not check_if_borrowed(item_model):
        raise InvalidLibraryItem(f"Item with ID {item_id} is not checked out")
    fines_to_add = check_if_returned_late(item_model, time_returned)
    fines_to_add_with_discount = fines_to_add - (
        fines_to_add * patron_model.fine_discount
    )
    update_libray_items_info_in_db(
        item_model,
        **{
            "borrower": None,
            "borrowed_status": False,
            "borrowed_at": None,
        },
    )
    update_patron_info_in_db(
        patron_model, "fines", patron_model.fines + fines_to_add_with_discount
    )
    transaction_id = Transaction(
        patron=patron_model,
        library_item=item_model,
        action=Actions.RETURNED.value,
        timestamp=time_returned,
    ).send_log_to_db()

    return transaction_id


def get_all_library_items(limit: int, skip: int) -> [LibraryItem]:
    """returns array of all library items
    Args:
        limit(int): how many results to return
        skip(int): how many results to skip

    Returns:
        [LibraryItem]: array of all library items in library
    """

    model_list = get_all_library_items_from_db(limit, skip)
    response_list = []
    model_factory = LibraryItemModelFactory()
    for item_model in model_list:
        response_list.append(
            model_factory.create_basemodel(library_item_model=item_model)
        )
    return response_list


def search_library_items(query_string: str, limit: int, skip: int) -> [LibraryItem]:
    """Query db for documents that match a string and convert them to basemodel

    Args:
        query_string (str): string to search for
        limit(int): how many results to return
        skip(int): how many results to skip

    Returns:
        [LibraryItemInternal]: array of library items that match query
    """
    M = LibraryItemModelFactory()
    return [
        M.create_basemodel(library_item)
        for library_item in search_library_items_in_db(query_string, limit, skip)
    ]
