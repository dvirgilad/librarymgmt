""" Bussiness logic layer for library items """
from datetime import datetime, timedelta
from library_item.library_item_model import (
    LibraryItemModel,
    LibraryItemBase,
    DiskModel,
    BookModel,
    DiskBase,
    BookBase,
)
from library_item.library_item_base import LibraryItemTypes
from library.library_dal import add_to_db, remove_from_db
from library.library import ProtectedAttribute
from library_item.library_item_dal import (
    get_all_library_items_from_db,
    get_library_item_from_db,
    update_libray_items_info_in_db,
    search_library_items_in_db,
)
from patrons.patron_controller import search_for_patron
from patrons.patron_dal import update_patron_info_in_db
from transactions.transactions import Transaction, Actions


class InvalidLibraryItem(Exception):
    """Exception raise if library item is invalid"""


class LibraryItemNotFound(Exception):
    """Exception raised if library item not found in library"""


class LibraryItemModelFactory:
    """Patron model factory class"""

    def create_model(self, library_item: LibraryItemBase):
        """creates library_item document model from basemodel

        Args:
            patron (LibraryItemBase): library_item basemodel

        Returns:
            _type_: library_item document model
        """
        match library_item.category:
            case LibraryItemTypes.BOOK.name:
                db_model = BookModel(**library_item.model_dump())
            case LibraryItemTypes.DISK.name:
                db_model = DiskModel(**library_item.model_dump())
            case default:
                db_model = LibraryItemModel(**library_item.model_dump())
        return db_model

    def create_basemodel(self, library_item_model: LibraryItemModel):
        """generates library item basemodel from document model

        Args:
            patron_model (PatronModel): patron document model

        Returns:
            _type_: patron basemodel
        """
        match library_item_model.category:
            case LibraryItemTypes.BOOK.name:
                patron_basemodel = BookBase(**library_item_model.to_json())
            case LibraryItemTypes.DISK.name:
                patron_basemodel = DiskBase(**library_item_model.to_json())
            case default:
                patron_basemodel = LibraryItemBase(**library_item_model.to_json())
        return patron_basemodel


def create_library_item(library_item: LibraryItemBase) -> str:
    """adds library item to db and returns its mongo ID

    Args:
        library_item (LibraryItemBase): Library item basemodel

    Returns:
        str: library items mongo ID
    """

    db_model = LibraryItemModelFactory().create_model(library_item=library_item)
    if check_if_borrowed(library_item):
        raise InvalidLibraryItem("Library item cannot be borrowed when it is added")
    patron_id = add_to_db(db_model)
    return patron_id


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
        raise LibraryItemNotFound(f"Library item with ID: {item_id} not found in DB")
    return patron_db_model


def remove_library_item(item_id: str) -> None:
    """Checks if library item exists in db and deletes it

    Args:
        item_id (str): Item mongo id
    """
    library_item_model = search_for_library_item_by_id(item_id)
    if check_if_borrowed(library_item_model):
        raise InvalidLibraryItem("Cannot delete an item that is currently checked out")
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


def get_library_item(item_id: str) -> LibraryItemBase:
    """searches for library item and returns its basemodel

    Args:
        item_id (str): item mongo ID

    Returns:
        LibraryItemBase: Item basemodel
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
    print(library_item.borrower)
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
    Returns:
        str: mongo id of transaction
    """
    patron_model = search_for_patron(borrower_id)
    item_model = search_for_library_item_by_id(item_id)
    time_borrowed = datetime.now()
    if check_if_borrowed(item_model):
        raise InvalidLibraryItem(f"Item with ID {item_id} is already borrowed!")
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
    ).send_to_mongo()
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
    time_difference = timedelta(time_returned - library_item.borrowed_at).seconds
    if time_difference > library_item.borrowing_period:
        return time_difference * library_item.fine
    return 0


def return_library_item(item_id: str) -> str:
    """Returns an item to the library

    Args:
        item_id (str): mongo id of library id

    Returns:
        str: mongo id of transaction
    """
    item_model = search_for_library_item_by_id(item_id)
    patron_model = item_model.borrower
    time_returned = datetime.now()
    if not check_if_borrowed(item_model):
        raise InvalidLibraryItem(f"Item with ID {item_id} is not checked out")
    fines_to_add = check_if_returned_late(item_model, time_returned)
    update_libray_items_info_in_db(
        item_model,
        **{
            "borrower": None,
            "borrowed_status": False,
            "borrowed_at": time_returned,
        },
    )
    update_patron_info_in_db(patron_model, "fines", patron_model.fines + fines_to_add)
    transaction_id = Transaction(
        patron=patron_model,
        library_item=item_model,
        action=Actions.RETURNED.value,
        timestamp=time_returned,
    ).send_to_mongo()

    return transaction_id


def get_all_library_items() -> [LibraryItemBase]:
    """returns array of all library items

    Returns:
        [LibraryItemBase]: array of all library items in library
    """
    model_list = get_all_library_items_from_db()
    response_list = []
    model_factory = LibraryItemModelFactory()
    for item_model in model_list:
        response_list.append(
            model_factory.create_basemodel(library_item_model=item_model)
        )
    return response_list


def search_library_items(query_string: str) -> [LibraryItemBase]:
    model_list = search_library_items_in_db(query_string)
    response_list = []
    M = LibraryItemModelFactory()
    for item_model in model_list:
        response_list.append(M.create_basemodel(item_model))
    return response_list
