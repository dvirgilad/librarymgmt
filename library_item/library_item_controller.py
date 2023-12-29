""" Bussiness logic layer for library items """
from mongoengine import ValidationError
from datetime import datetime
from library_item.dal.library_item_model import (
    LibraryItemReturn,
    LibraryItemCreate,
    LibraryItemEdit,
)
from library_item.dal.library_item_document import LibraryItemModel
from library_item.library_item_exceptions import LibraryItemNotFound, InvalidLibraryItem
from library.library_dal import add_to_db, remove_from_db
from library.library_exceptions import AppException, InvalidID
from library_item.dal.library_item_dal import (
    get_all_library_items_from_db,
    get_library_item_from_db,
    update_libray_items_info_in_db,
    search_library_items_in_db,
)
from patrons.patron_controller import search_for_patron
from patrons.dal.patron_dal import update_patron_info_in_db
from transactions.transactions import Transaction, Actions
from library_item.library_item_model_factory import LibraryItemModelFactory


def create_library_item(library_item: LibraryItemCreate) -> str:
    """Convert a libarry item basemodel to a document adn add it to db

    :param library_item: library item basemodel to add
    :type library_item: LibraryItemCreate
    :return: object ID of model
    :rtype: str
    """
    try:
        db_model = LibraryItemModelFactory.create_model(library_item=library_item)
        item_id = add_to_db(db_model)
        return item_id
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def search_for_library_item_by_id(item_id: str) -> LibraryItemModel:
    """Search for library item by ID

    :param item_id: object id of item
    :type item_id: str
    :raises LibraryItemNotFound: if item is not found
    :raises InvalidID: if ID given is not valid
    :return: Library item document
    :rtype: LibraryItemModel
    """
    try:
        patron_db_model = get_library_item_from_db(item_id)
    except ValidationError as exc:
        raise InvalidID(object_id=item_id) from exc
    if patron_db_model is None:
        raise LibraryItemNotFound(item_id)
    return patron_db_model


def remove_library_item(item_id: str) -> None:
    """searches for a library item and deletes it

    :param item_id: ID of item to delete
    :type item_id: str
    :raises InvalidLibraryItem: If item is currently checked
    :raises AppException: generic exception
    """
    library_item_model = search_for_library_item_by_id(item_id)
    if check_if_borrowed(library_item_model):
        raise InvalidLibraryItem(
            item_id, "Cannot delete an item that is currently checked out"
        )
    try:
        remove_from_db(library_item_model)
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def update_library_item(item_id: str, new_item_info: LibraryItemEdit) -> None:
    """search for library item and update its info

    :param item_id: ID of item to edit
    :type item_id: str
    :param new_item_info: basemodel of attributes to update
    :type new_item_info: LibraryItemEdit
    :raises AppException: generic exception
    """

    patron_model = search_for_library_item_by_id(item_id)
    try:
        update_libray_items_info_in_db(
            patron_model, **new_item_info.model_dump(exclude_none=True)
        )
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def get_library_item(item_id: str) -> LibraryItemReturn:
    """gets library item and converts it to basemodel

    :param item_id: object id of item
    :type item_id: str
    :raises AppException: generic exception
    :return: library item basemodel
    :rtype: LibraryItemReturn
    """
    item_model = search_for_library_item_by_id(item_id=item_id)
    try:
        item_basemodel = LibraryItemModelFactory.create_basemodel(item_model)
        return item_basemodel
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def check_if_borrowed(library_item: LibraryItemModel) -> bool:
    """Check if item is currently checked out

    :param library_item: library item to check
    :type library_item: LibraryItemModel
    :return: If item is checked out
    :rtype: bool
    """
    if (
        library_item.borrowed_status
        or library_item.borrower is not None
        or library_item.borrowed_at is not None
    ):
        return True
    return False


def borrow_item(item_id: str, borrower_id: str) -> str:
    """Check if a library item can be borrowed and then borrows it

    :param item_id: ID of item to borrow
    :type item_id: str
    :param borrower_id: ID of patron that is borrowing
    :type borrower_id: str
    :raises InvalidLibraryItem: If item cannot be borrowed
    :return: ID of transaction
    :rtype: str
    """
    patron_model = search_for_patron(borrower_id)
    item_model = search_for_library_item_by_id(item_id)
    time_borrowed = datetime.utcnow()
    if check_if_borrowed(item_model):
        raise InvalidLibraryItem(
            item_id, f"Item with ID {item_id} is already borrowed!"
        )
    try:
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
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def check_fine_amount(library_item: LibraryItemModel, time_returned: datetime) -> int:
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
    """Checks if library item is borrowed and returns it

    :param item_id: ID of item to return
    :type item_id: str
    :raises InvalidLibraryItem: if item is not borrowed
    :return: ID of transaction
    :rtype: str
    """
    item_model = search_for_library_item_by_id(item_id)
    patron_model = item_model.borrower
    time_returned = datetime.utcnow()
    if not check_if_borrowed(item_model):
        raise InvalidLibraryItem(f"Item with ID {item_id} is not checked out")
    try:
        fines_to_add = check_fine_amount(item_model, time_returned)
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
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def get_all_library_items(limit: int, skip: int) -> dict:
    """Returns requested amount of library items

    :raises AppException: generic exception
    :return: dict of library items
    :rtype: dict
    """
    try:
        model_list = get_all_library_items_from_db(limit, skip)

        return {
            "items": [
                LibraryItemModelFactory.create_basemodel(library_item_model=item_model)
                for item_model in model_list
            ],
            "limit": limit,
            "skip": skip,
        }
    except Exception as exc:
        raise AppException(500, str(exc)) from exc


def search_library_items(query_string: str, limit: int, skip: int) -> dict:
    """Search db for a string

    :param query_string: string to search for
    :type query_string: str
    :param limit: number of items to return
    :type limit: int
    :param skip: number of items to return
    :type skip: int
    :return: dict of items
    :rtype: dict
    """
    return {
        "items": [
            LibraryItemModelFactory.create_basemodel(library_item)
            for library_item in search_library_items_in_db(query_string, limit, skip)
        ],
        "limit": limit,
        "skip": skip,
    }
