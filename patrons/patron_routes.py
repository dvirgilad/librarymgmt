"""patron fastapi routes"""
from fastapi import APIRouter, HTTPException, status
from patrons.patron_controller import (
    get_patron,
    create_patron,
    remove_patron,
    update_patron,
    get_all_patrons,
    PatronNotFound,
    ProtectedAttribute,
)
from patrons.patron_model import Patron, PatronBase

PATRON_ROUTER = APIRouter()


@PATRON_ROUTER.get("/{patron_id}")
def get_patron_route(patron_id: str) -> Patron:
    """Route to get a specific patron by ID

    Args:
        patron_id (str): the ID of the patron

    Returns:
        Patron: Patron model
    """
    try:
        return get_patron(patron_id)
    except PatronNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patron not found"
        ) from exc


@PATRON_ROUTER.get("/")
def get_all_patrons_route(limit: int = 10, skip: int = 0) -> {}:
    """Returns array of all patrons

    Returns:
        {}: patron array
    """
    return {"items": get_all_patrons(), "limit": limit, "skip": skip}


@PATRON_ROUTER.post("/", response_model=str)
def post_patron_route(patron: PatronBase) -> str:
    """Route to create a patron

    Args:
        patron (Student | Teacher): the patron model

    Returns:
        str: patron ID
    """
    return create_patron(patron)


@PATRON_ROUTER.delete("/{patron_id}")
def delete_patron_route(patron_id: str) -> None:
    """Deletes a patron by ID

    Args:
        patron_id (str): patron ID
    """
    try:
        remove_patron(patron_id)
    except PatronNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patron not found"
        ) from exc


@PATRON_ROUTER.patch("/{patron_id}")
def update_patron_route(patron_id: str, attribute_to_edit: str, new_value: str) -> None:
    """update the value of a specific patron attribute

    Args:
        patron_id (str): ID of patron to edit
        attribute_to_edit (str): attribute to edit
        new_value (str): new value of attribute
    Raises:
        HTTPException: ProtectedAttribute
    """
    try:
        update_patron(patron_id, attribute_to_edit, new_value)
    except ProtectedAttribute as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"cannot edit a patrons {attribute_to_edit}",
        ) from exc
