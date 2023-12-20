from fastapi import APIRouter, HTTPException, status
from library_item.library_item_controller import (
    create_library_item,
    get_all_library_items,
    get_library_item,
    remove_library_item,
    update_library_item,
    return_library_item,
    borrow_item,
    search_library_items,
    LibraryItemNotFound,
    InvalidLibraryItem,
    ProtectedAttribute,
)
from library_item.library_item_model import LibraryItem, LibraryItemBase


LIBRARY_ITEM_ROUTER = APIRouter()
LIBRARY_ACTIONS_ROUTER = APIRouter()


@LIBRARY_ITEM_ROUTER.get("/")
def get_all_library_items_route(limit: int = 10, skip: int = 0) -> {}:
    """Returns all library items
    Args:
        limit(int): how many results to return
        skip(int): how many results to skip

    Raises:
        HTTPException: _description_

    Returns:
        {}: dict of results
    """
    if limit < 1 or skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid limit or skip"
        )
    return {"items": get_all_library_items(limit, skip), "limit": limit, "skip": skip}


@LIBRARY_ITEM_ROUTER.get("/{item_id}")
def get_library_item_route(item_id: str) -> LibraryItem:
    """Get a library item by id

    Args:
        item_id (str): library item id

    Raises:
        HTTPException: Librray item not found

    Returns:
        LibraryItem: libray item model
    """
    try:
        return get_library_item(item_id)
    except LibraryItemNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library item with ID {item_id} not found",
        ) from exc


@LIBRARY_ITEM_ROUTER.post("/")
def post_library_item_route(library_item: LibraryItemBase) -> str:
    """Route to create a library item

    Args:
        library_item (LibraryItemBase): library item to add

    Returns:
        str: library item ID
    """
    return create_library_item(library_item)


@LIBRARY_ITEM_ROUTER.delete("/{item_id}")
def delete_library_item_route(item_id: str) -> None:
    """Route to delete a library item

    Args:
        item_id (str): library item ID

    Raises:
        HTTPException: LibraryItemNotFound
        HTTPException: InvalidLibraryItem
    """
    try:
        remove_library_item(item_id)
    except LibraryItemNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library item with ID {item_id} not found",
        ) from exc
    except InvalidLibraryItem as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Library item with ID {item_id} cannot be deleted as it is checked out",
        ) from exc


@LIBRARY_ITEM_ROUTER.patch("/{item_id}")
def update_library_item_route(
    item_id: str, attribute_to_edit: str, new_value: str
) -> None:
    """Route to update the value of a specific library item attribute

    Args:
        item_id (str): ID of library item to edit
        attribute_to_edit (str): attribute to edit
        new_value (str): new value of attribute

    Raises:
        HTTPException: ProtectedAttribute
    """
    try:
        update_library_item(item_id, attribute_to_edit, new_value)
    except ProtectedAttribute as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"cannot edit a library items {attribute_to_edit}",
        ) from exc


@LIBRARY_ACTIONS_ROUTER.post("/borrow")
def borrow_item_route(item_id: str, patron_id: str) -> str:
    """Route to borrow item

    Args:
        item_id (str): item of item to borrow
        patron_id (str): id of borrower

    Raises:
        HTTPException: If item is already borrowed

    Returns:
        str: Transaction ID
    """
    try:
        return borrow_item(item_id, patron_id)
    except InvalidLibraryItem as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"library item with id {item_id} is already borrowed",
        ) from exc


@LIBRARY_ACTIONS_ROUTER.post("/return/{item_id}")
def return_item_route(item_id: str) -> str:
    """Route to return item to library

    Args:
        item_id (str): ID of item to return

    Raises:
        HTTPException: if item is not borrowed

    Returns:
        str: transaction ID
    """
    try:
        return return_library_item(item_id)
    except InvalidLibraryItem as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"library item with id {item_id} is not borrowed",
        ) from exc


@LIBRARY_ACTIONS_ROUTER.get("/search/{query_string}")
def search_library_items_route(query_string: str, limit: int = 10, skip: int = 0) -> {}:
    """route to search for library item by a string

    Args:
        query_string (str): string to search for
        limit(int): how many results to return
        skip(int): how many results to skip

    Returns:
        [LibraryItemInternal]: Array of all library items that match query
    """
    if limit < 1 or skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid limit or skip"
        )
    return {
        "items": search_library_items(query_string, limit, skip),
        "limit": limit,
        "skip": skip,
    }
