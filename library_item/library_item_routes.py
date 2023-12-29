from typing import Annotated
from fastapi import APIRouter, Query

from library_item.library_item_controller import (
    borrow_item,
    create_library_item,
    get_all_library_items,
    get_library_item,
    remove_library_item,
    return_library_item,
    search_library_items,
    update_library_item,
)
from library_item.dal.library_item_model import (
    LibraryItemReturn,
    LibraryItemEdit,
    LibraryItemCreate,
)
from consts import PaginationDefaults

LIBRARY_ITEM_ROUTER = APIRouter()
LIBRARY_ACTIONS_ROUTER = APIRouter()


@LIBRARY_ITEM_ROUTER.get("/")
def get_all_library_items_route(
    limit: Annotated[
        int, Query(description="Number of items to return", ge=1)
    ] = PaginationDefaults.limit,
    skip: Annotated[
        int, Query(description="Number of items to skip", ge=0)
    ] = PaginationDefaults.skip,
) -> dict:
    """Route to get requested amount of library items

    :return: dict of items
    :rtype: dict
    """

    return get_all_library_items(limit, skip)


@LIBRARY_ITEM_ROUTER.get("/{item_id}")
def get_library_item_route(item_id: str) -> LibraryItemReturn:
    """Route to get library item by id

    :param item_id: object ID of item
    :type item_id: str
    :return: Library item basemodel
    :rtype: LibraryItemReturn
    """
    return get_library_item(item_id)


@LIBRARY_ITEM_ROUTER.post("/")
def post_library_item_route(library_item: LibraryItemCreate) -> str:
    """Route to add a library item

    :param library_item: Library item model
    :type library_item: LibraryItemCreate
    :return: Item object ID
    :rtype: str
    """
    return create_library_item(library_item)


@LIBRARY_ITEM_ROUTER.delete("/{item_id}")
def delete_library_item_route(item_id: str) -> None:
    """Route to delete a library item by ID

    :param item_id: ID of to delete
    :type item_id: str
    """
    remove_library_item(item_id)


@LIBRARY_ITEM_ROUTER.patch("/{item_id}")
def update_library_item_route(item_id: str, updated_item: LibraryItemEdit) -> None:
    """Route to update a library item

    :param item_id: ID of item to edit
    :type item_id: str
    :param updated_item: dict of attributes to edit
    :type updated_item: LibraryItemEdit
    """
    update_library_item(item_id, updated_item)


@LIBRARY_ACTIONS_ROUTER.post("/borrow")
def borrow_item_route(item_id: str, patron_id: str) -> str:
    """Route to borrow and item from library

    :param item_id: ID of item to borrow
    :type item_id: str
    :param patron_id: ID of patron borrowing the item
    :type patron_id: str
    :return: transaction ID
    :rtype: str
    """
    return borrow_item(item_id, patron_id)


@LIBRARY_ACTIONS_ROUTER.post("/return/{item_id}")
def return_item_route(item_id: str) -> str:
    """Route to return an item to the library

    :param item_id: ID of item to return
    :type item_id: str
    :return: ID of transaction
    :rtype: str
    """
    return return_library_item(item_id)


@LIBRARY_ACTIONS_ROUTER.get("/search/{query_string}")
def search_library_items_route(
    query_string: str,
    limit: Annotated[
        int, Query(description="Number of items to return", ge=1)
    ] = PaginationDefaults.limit,
    skip: Annotated[
        int, Query(description="Number of items to skip", ge=0)
    ] = PaginationDefaults.skip,
) -> dict:
    """Search a library for a string

    :param query_string: String to search for
    :type query_string: str
    :return: results of search
    :rtype: dict
    """

    return search_library_items(query_string, limit, skip)
